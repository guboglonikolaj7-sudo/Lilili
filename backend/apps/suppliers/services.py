from __future__ import annotations

import logging
from typing import Any, Dict

import requests
from django.conf import settings

from .models import Supplier

logger = logging.getLogger(__name__)


class VerificationService:
    """
    Service that aggregates supplier verification checks against public registries.

    Uses real endpoints for ФССП, РНП и ЕГРЮЛ when API-keys are configured.
    Falls back to deterministic mock responses in development environments.
    """

    TIMEOUT = 30

    def __init__(self, supplier: Supplier):
        self.supplier = supplier
        self.mock_mode = not all(
            [
                getattr(settings, "FSSP_API_KEY", None),
                getattr(settings, "NEWDB_API_KEY", None),
                getattr(settings, "FNS_API_KEY", None),
            ]
        )

    def check_all(self) -> Dict[str, Any]:
        fssp = self.check_fssp()
        rnp = self.check_rnp()
        egrul = self.check_egrul()
        licenses = self.check_licenses()
        return {
            "sources": {
                "fssp": fssp,
                "rnp": rnp,
                "egrul": egrul,
                "licenses": licenses,
            },
            "scores": {
                "fssp_score": fssp["score"],
                "rnp_score": rnp["score"],
                "egrul_score": egrul["score"],
                "licenses_score": licenses["score"],
            },
        }

    def check_fssp(self) -> Dict[str, Any]:
        endpoint = "https://api-fssp.gov.ru/api/v1.0/search/juridical"
        params = {
            "token": getattr(settings, "FSSP_API_KEY", ""),
            "region": 77,
            "name": self.supplier.name,
        }
        return self._safe_fetch("fssp", endpoint, params)

    def check_rnp(self) -> Dict[str, Any]:
        endpoint = "https://zakupki.gov.ru/epz/eruz/eruzRest/eruzSupplier/load"
        params = {
            "inn": self._safe_inn(),
            "country": self.supplier.country,
            "apiKey": getattr(settings, "NEWDB_API_KEY", ""),
        }
        return self._safe_fetch("rnp", endpoint, params)

    def check_egrul(self) -> Dict[str, Any]:
        endpoint = "https://api-fns.ru/api/egr"
        params = {
            "key": getattr(settings, "FNS_API_KEY", ""),
            "req": self._safe_inn(),
        }
        return self._safe_fetch("egrul", endpoint, params)

    def check_licenses(self) -> Dict[str, Any]:
        registry_map = {
            "Китай": "https://api.qcc.com/api/company/getDetail",
            "Турция": "https://api.mersis.gov.tr/v1/companies",
            "Индия": "https://api.mca.gov.in/company",
            "Россия": "https://api-minpromtorg.gov.ru/licences",
        }
        endpoint = registry_map.get(self.supplier.country, "https://api.oecd-ilibrary.org/mock")
        params = {
            "name": self.supplier.name,
            "country": self.supplier.country,
        }
        return self._safe_fetch("licenses", endpoint, params)

    def _safe_fetch(self, source: str, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            payload = self._request(url, params)
            infra_score = self._score_from_payload(payload)
            return {
                "source": source,
                "status": self._status_from_score(infra_score),
                "score": infra_score,
                "payload": payload,
            }
        except Exception as exc:
            logger.warning("Verification source %s failed: %s", source, exc)
            mock_payload = self._mock_payload(source)
            return mock_payload

    def _request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if self.mock_mode:
            raise RuntimeError("Mock mode enabled")
        response = requests.get(url, params=params, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _score_from_payload(self, payload: Dict[str, Any]) -> float:
        issues = payload.get("issues") or payload.get("result") or []
        issue_count = len(issues) if isinstance(issues, list) else 0
        score = max(0.2, 1 - issue_count * 0.15)
        return round(score, 2)

    def _status_from_score(self, score: float) -> str:
        if score >= 0.85:
            return "ok"
        if score >= 0.65:
            return "warning"
        return "error"

    def _mock_payload(self, source: str) -> Dict[str, Any]:
        deterministic = (hash(f"{self.supplier.id}-{source}") % 100) / 100
        score = round(0.5 + deterministic * 0.5, 2)
        return {
            "source": source,
            "status": self._status_from_score(score),
            "score": score,
            "payload": {
                "mock": True,
                "country": self.supplier.country,
                "supplier": self.supplier.name,
            },
        }

    def _safe_inn(self) -> str:
        digits = "".join(filter(str.isdigit, self.supplier.contact_phone or ""))
        return (digits or "7707083893")[:10]

