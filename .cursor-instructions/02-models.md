обавь в models.py:
- модель VerificationCheck с полями баллов (fssp/rnp/egrul/licenses), overall_score, статусами, risk_level, JSON checked_sources, error_message, timestamps.
- перечисления VerificationStatus и VerificationRiskLevel.
- в Supplier новые поля verification_status, verification_score, is_verified, last_verified_at + индексы.
- метод Supplier.apply_verification_result и VerificationCheck.calculate_overall_score (Decimal round, risk logic).