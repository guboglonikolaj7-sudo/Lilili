from django.db import models


class Category(models.Model):
    name = models.CharField("Категория", max_length=100, unique=True)
    slug = models.SlugField("Слаг", unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
       

    def __str__(self):
        return self.name


class LogisticsCompany(models.Model):
    name = models.CharField("Логистическая компания", max_length=150)
    site = models.URLField("Сайт", blank=True)

    class Meta:
        verbose_name = "Логистическая компания"
        verbose_name_plural = "Логистические компании"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField("Название", max_length=150)
    country = models.CharField("Страна", max_length=100)
    city = models.CharField("Город", max_length=100)
    description = models.TextField("Описание", blank=True)
    logo = models.ImageField("Логотип", upload_to="logos/", blank=True)
    video_url = models.URLField("YouTube-видео", blank=True)
    moq = models.PositiveIntegerField("Мин. заказ (MOQ)", default=1)
    contact_email = models.EmailField("Контактный email", blank=True)
    contact_phone = models.CharField("Контактный телефон", max_length=20, blank=True)
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="suppliers",
    )
    logistics_options = models.ManyToManyField(LogisticsCompany, blank=True)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name