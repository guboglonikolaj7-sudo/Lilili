from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.core.validators import MinValueValidator, URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Category(models.Model):
    name = models.CharField("Категория", max_length=100, unique=True)
    slug = models.SlugField("Слаг", unique=True)
    description = models.TextField("Описание", blank=True)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

class LogisticsCompany(models.Model):
    name = models.CharField("Логистическая компания", max_length=150, unique=True)
    site = models.URLField("Сайт", blank=True, validators=[URLValidator()])
    description = models.TextField("Описание", blank=True)
    
    class Meta:
        verbose_name = "Логистическая компания"
        verbose_name_plural = "Логистические компании"
        ordering = ["name"]

    def __str__(self):
        return self.name

class VerificationStatus(models.TextChoices):
    NOT_STARTED = "not_started", "Не запущена"
    IN_PROGRESS = "in_progress", "В процессе"
    COMPLETED = "completed", "Завершена"
    FAILED = "failed", "Ошибка"


class VerificationRiskLevel(models.TextChoices):
    LOW = "low", "Низкий"
    MEDIUM = "medium", "Средний"
    HIGH = "high", "Высокий"


class Supplier(models.Model):
    name = models.CharField("Название", max_length=150)
    country = models.CharField("Страна", max_length=100)
    city = models.CharField("Город", max_length=100)
    description = models.TextField("Описание", blank=True)
    logo = models.ImageField("Логотип", upload_to="suppliers/logos/%Y/%m/", blank=True)
    video_url = models.URLField("YouTube-видео", blank=True, validators=[URLValidator()])
    moq = models.PositiveIntegerField("Мин. заказ (MOQ)", default=1, validators=[MinValueValidator(1)])
    contact_email = models.EmailField("Контактный email", blank=True)
    contact_phone = models.CharField("Контактный телефон", max_length=20, blank=True)
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="suppliers",
        verbose_name="Категория"
    )
    logistics_options = models.ManyToManyField(
        LogisticsCompany, 
        blank=True, 
        verbose_name="Варианты логистики"
    )
    
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    is_active = models.BooleanField("Активен", default=True)
    verification_status = models.CharField(
        "Статус проверки",
        max_length=32,
        choices=VerificationStatus.choices,
        default=VerificationStatus.NOT_STARTED,
    )
    verification_score = models.DecimalField(
        "Итоговый балл проверки",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
    )
    is_verified = models.BooleanField("Проверен", default=False)
    last_verified_at = models.DateTimeField("Дата проверки", blank=True, null=True)
    
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["country", "city"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active", "created_at"]),
            models.Index(fields=["verification_status"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.country})"
    
    def clean(self):
        if self.video_url and "youtube.com" not in self.video_url and "youtu.be" not in self.video_url:
            raise ValidationError({"video_url": "Только YouTube URL разрешены"})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def apply_verification_result(self, check: "VerificationCheck") -> None:
        self.verification_status = check.status
        self.verification_score = check.overall_score
        self.is_verified = check.is_verified
        self.last_verified_at = check.completed_at or timezone.now()
        self.save(
            update_fields=[
                "verification_status",
                "verification_score",
                "is_verified",
                "last_verified_at",
            ]
        )


class VerificationCheck(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="verification_checks",
        verbose_name="Поставщик",
    )
    country = models.CharField("Страна проверки", max_length=100)
    status = models.CharField(
        "Статус",
        max_length=32,
        choices=VerificationStatus.choices,
        default=VerificationStatus.IN_PROGRESS,
    )
    fssp_score = models.DecimalField(
        "ФССП балл", max_digits=4, decimal_places=2, blank=True, null=True
    )
    rnp_score = models.DecimalField(
        "РНП балл", max_digits=4, decimal_places=2, blank=True, null=True
    )
    egrul_score = models.DecimalField(
        "ЕГРЮЛ балл", max_digits=4, decimal_places=2, blank=True, null=True
    )
    licenses_score = models.DecimalField(
        "Лицензии балл", max_digits=4, decimal_places=2, blank=True, null=True
    )
    overall_score = models.DecimalField(
        "Итоговый балл", max_digits=4, decimal_places=2, blank=True, null=True
    )
    is_verified = models.BooleanField("Поставщик подтвержден", default=False)
    risk_level = models.CharField(
        "Уровень риска",
        max_length=16,
        choices=VerificationRiskLevel.choices,
        blank=True,
        null=True,
    )
    checked_sources = models.JSONField("Источники", default=dict, blank=True)
    error_message = models.TextField("Ошибка", blank=True)
    started_at = models.DateTimeField("Начато", auto_now_add=True)
    completed_at = models.DateTimeField("Завершено", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Проверка поставщика"
        verbose_name_plural = "Проверки поставщиков"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["supplier", "status"]),
            models.Index(fields=["risk_level"]),
        ]

    def __str__(self) -> str:
        return f"{self.supplier.name} — {self.status}"

    def calculate_overall_score(self) -> Decimal | None:
        scores = [
            score
            for score in [
                self.fssp_score,
                self.rnp_score,
                self.egrul_score,
                self.licenses_score,
            ]
            if score is not None
        ]
        if not scores:
            self.overall_score = None
            self.is_verified = False
            self.risk_level = None
            return None

        aggregated = sum(scores) / Decimal(len(scores))
        self.overall_score = aggregated.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        if self.overall_score >= Decimal("0.85"):
            self.risk_level = VerificationRiskLevel.LOW
        elif self.overall_score >= Decimal("0.65"):
            self.risk_level = VerificationRiskLevel.MEDIUM
        else:
            self.risk_level = VerificationRiskLevel.HIGH

        self.is_verified = self.overall_score >= Decimal("0.75")
        return self.overall_score

    def save(self, *args, **kwargs):
        self.calculate_overall_score()
        super().save(*args, **kwargs)
