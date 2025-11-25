from django.db import models
from django.core.validators import MinValueValidator, URLValidator
from django.core.exceptions import ValidationError

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
    
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["country", "city"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active", "created_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.country})"
    
    def clean(self):
        if self.video_url and "youtube.com" not in self.video_url and "youtu.be" not in self.video_url:
            raise ValidationError({"video_url": "Только YouTube URL разрешены"})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
