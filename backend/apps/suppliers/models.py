from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.core.validators import MinValueValidator, URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Category(models.Model):
    """Иерархическая категория товаров и услуг"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Слаг", unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Родительская категория"
    )
    description = models.TextField("Описание", blank=True)
    icon = models.CharField("Иконка (emoji)", max_length=5, blank=True)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['parent__id', 'id']
        indexes = [
            models.Index(fields=['parent', 'slug']),
        ]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name

    def get_full_path(self):
        """Возвращает полный путь категории (например: 'Электроника → Смартфоны')"""
        if self.parent:
            return f"{self.parent.get_full_path()} → {self.name}"
        return self.name


class LogisticsCompany(models.Model):
    """Логистические компании для интеграции"""
    name = models.CharField("Название", max_length=150, unique=True)
    site = models.URLField("Сайт", blank=True, validators=[URLValidator()])
    description = models.TextField("Описание", blank=True)
    countries_served = models.JSONField("Обслуживаемые страны", default=list, blank=True)
    
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
    """Модель поставщика с верификацией и иерархическими категориями"""
    name = models.CharField("Название", max_length=150, db_index=True)
    country = models.CharField("Страна", max_length=100, db_index=True)
    city = models.CharField("Город", max_length=100, db_index=True)
    description = models.TextField("Описание", blank=True)
    logo = models.ImageField("Логотип", upload_to="suppliers/logos/%Y/%m/", blank=True)
    video_url = models.URLField("YouTube-видео", blank=True, validators=[URLValidator()])
    
    moq = models.PositiveIntegerField("Мин. заказ (MOQ)", default=1, validators=[MinValueValidator(1)])
    moq_currency = models.CharField("Валюта MOQ", max_length=3, default="USD", choices=[
        ("USD", "USD"),
        ("EUR", "EUR"),
        ("CNY", "CNY"),
        ("RUB", "RUB"),
    ])
    
    contact_email = models.EmailField("Контактный email", blank=True)
    contact_phone = models.CharField("Контактный телефон", max_length=20, blank=True)
    website = models.URLField("Сайт поставщика", blank=True, validators=[URLValidator()])
    
    # Иерархическая категория (можно привязать к любому уровню)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="suppliers",
        verbose_name="Категория"
    )
    
    # Дополнительные категории (для кросс-продуктовых поставщиков)
    additional_categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="additional_suppliers",
        verbose_name="Дополнительные категории"
    )
    
    logistics_options = models.ManyToManyField(
        LogisticsCompany, 
        blank=True, 
        verbose_name="Варианты логистики"
    )
    
    # Верификация
    verification_status = models.CharField(
        "Статус проверки",
        max_length=32,
        choices=VerificationStatus.choices,
        default=VerificationStatus.NOT_STARTED,
        db_index=True
    )
    verification_score = models.DecimalField(
        "Итоговый балл проверки",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        db_index=True
    )
    is_verified = models.BooleanField("Проверен", default=False, db_index=True)
    last_verified_at = models.DateTimeField("Дата проверки", blank=True, null=True)
    verification_expires_at = models.DateTimeField("Срок действия проверки", blank=True, null=True)
    
    # Бизнес-метрики
    is_active = models.BooleanField("Активен", default=True, db_index=True)
    is_premium = models.BooleanField("Премиум", default=False, help_text="Платный аккаунт поставщика")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    
    # RFQ-специфичные поля
    avg_response_time_hours = models.PositiveIntegerField("Среднее время ответа (часы)", null=True, blank=True)
    quote_acceptance_rate = models.DecimalField("Конверсия котировок", max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ["-is_premium", "-verification_score", "-created_at"]
        indexes = [
            models.Index(fields=["country", "city", "is_active"]),
            models.Index(fields=["category", "is_verified", "is_active"]),
            models.Index(fields=["verification_status"]),
            models.Index(fields=["is_premium"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.country})"
    
    def clean(self):
        if self.video_url and "youtube.com" not in self.video_url and "youtu.be" not in self.video_url:
            raise ValidationError({"video_url": "Только YouTube URL разрешены"})
        
        # Проверка срока действия верификации
        if self.verification_expires_at and self.last_verified_at:
            if self.verification_expires_at < self.last_verified_at:
                raise ValidationError({"verification_expires_at": "Срок действия не может быть раньше даты проверки"})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        
        # Автоматически вычисляем срок действия (90 дней для верифицированных)
        if self.is_verified and self.last_verified_at and not self.verification_expires_at:
            self.verification_expires_at = self.last_verified_at + timezone.timedelta(days=90)
        
        super().save(*args, **kwargs)

    def apply_verification_result(self, check: "VerificationCheck") -> None:
        """Применяет результат проверки к поставщику"""
        self.verification_status = check.status
        self.verification_score = check.overall_score
        self.is_verified = check.is_verified
        self.last_verified_at = check.completed_at or timezone.now()
        
        # Вычисляем срок действия
        if self.is_verified:
            self.verification_expires_at = self.last_verified_at + timezone.timedelta(days=90)
        
        self.save(
            update_fields=[
                "verification_status",
                "verification_score",
                "is_verified",
                "last_verified_at",
                "verification_expires_at",
            ]
        )
    
    def is_verification_expired(self) -> bool:
        """Проверяет, истекла ли верификация"""
        if not self.verification_expires_at:
            return True
        return timezone.now() > self.verification_expires_at
    
    def get_renewal_deadline(self) -> timezone.datetime | None:
        """Возвращает дату дедлайна для продления верификации"""
        if not self.verification_expires_at:
            return None
        # За 7 дней до истечения можно продлевать
        return self.verification_expires_at - timezone.timedelta(days=7)


class VerificationCheck(models.Model):
    """Модель для хранения результатов проверки поставщика"""
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="verification_checks",
        verbose_name="Поставщик",
        db_index=True
    )
    country = models.CharField("Страна проверки", max_length=100)
    
    status = models.CharField(
        "Статус",
        max_length=32,
        choices=VerificationStatus.choices,
        default=VerificationStatus.IN_PROGRESS,
        db_index=True
    )
    
    # Скоры по каждому реестру (0.00 - 1.00)
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
        db_index=True
    )
    
    # Детали проверки
    checked_sources = models.JSONField("Источники", default=dict, blank=True)
    error_message = models.TextField("Ошибка", blank=True)
    
    # Метрики времени
    started_at = models.DateTimeField("Начато", auto_now_add=True)
    completed_at = models.DateTimeField("Завершено", blank=True, null=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Проверка поставщика"
        verbose_name_plural = "Проверки поставщиков"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["supplier", "status"]),
            models.Index(fields=["country", "risk_level"]),
            models.Index(fields=["is_verified", "completed_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.supplier.name} — {self.status} ({self.country})"

    def calculate_overall_score(self) -> Decimal | None:
        """Вычисляет итоговый скор на основе доступных проверок"""
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

        # Определяем уровень риска
        if self.overall_score >= Decimal("0.85"):
            self.risk_level = VerificationRiskLevel.LOW
        elif self.overall_score >= Decimal("0.65"):
            self.risk_level = VerificationRiskLevel.MEDIUM
        else:
            self.risk_level = VerificationRiskLevel.HIGH

        # Порог верификации
        self.is_verified = self.overall_score >= Decimal("0.75")
        return self.overall_score

    def mark_as_completed(self) -> None:
        """Завершает проверку и применяет результат к поставщику"""
        self.completed_at = timezone.now()
        self.status = VerificationStatus.COMPLETED
        self.calculate_overall_score()
        self.save()
        
        # Применяем результат к поставщику
        self.supplier.apply_verification_result(self)

    def mark_as_failed(self, error_message: str) -> None:
        """Помечает проверку как неудачную"""
        self.error_message = error_message
        self.status = VerificationStatus.FAILED
        self.completed_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        # Автоматически пересчитываем скор при сохранении
        if self.status == VerificationStatus.COMPLETED:
            self.calculate_overall_score()
        super().save(*args, **kwargs)