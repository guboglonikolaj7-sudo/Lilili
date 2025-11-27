from __future__ import annotations

import logging
from typing import Iterable

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import Supplier, VerificationCheck, VerificationStatus
from .services import VerificationService

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def verify_supplier_task(self, supplier_id: int) -> int:
    supplier = Supplier.objects.select_for_update().get(pk=supplier_id)
    service = VerificationService(supplier)

    with transaction.atomic():
        supplier.verification_status = VerificationStatus.IN_PROGRESS
        supplier.save(update_fields=["verification_status"])
        check = VerificationCheck.objects.create(
            supplier=supplier,
            country=supplier.country,
            status=VerificationStatus.IN_PROGRESS,
        )

    try:
        payload = service.check_all()
        scores = payload["scores"]
        check.checked_sources = payload["sources"]
        check.fssp_score = scores["fssp_score"]
        check.rnp_score = scores["rnp_score"]
        check.egrul_score = scores["egrul_score"]
        check.licenses_score = scores["licenses_score"]
        check.status = VerificationStatus.COMPLETED
        check.completed_at = timezone.now()
        check.save()

        supplier.refresh_from_db()
        supplier.apply_verification_result(check)
        logger.info("Supplier %s verified via task %s", supplier_id, self.request.id)
        return check.id
    except Exception as exc:
        logger.error("Verification failed for supplier %s: %s", supplier_id, exc)
        check.status = VerificationStatus.FAILED
        check.error_message = str(exc)
        check.completed_at = timezone.now()
        check.save(update_fields=["status", "error_message", "completed_at", "updated_at"])

        supplier.verification_status = VerificationStatus.FAILED
        supplier.is_verified = False
        supplier.save(update_fields=["verification_status", "is_verified"])
        raise


@shared_task
def batch_verify_suppliers(supplier_ids: Iterable[int] | None = None) -> int:
    ids = (
        list(supplier_ids)
        if supplier_ids
        else list(
            Supplier.objects.filter(is_active=True).values_list("id", flat=True)
        )
    )
    for supplier_id in ids:
        verify_supplier_task.delay(supplier_id)
    return len(ids)

