from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
        ('on_hold', 'На удержании'),
    ]
    
    title = models.CharField("Название заказа", max_length=200)
    description = models.TextField("Описание")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    category = models.ForeignKey(
        'suppliers.Category', 
        on_delete=models.PROTECT, 
        null=True,
        verbose_name="Категория"
    )
    budget_min = models.DecimalField(
        "Мин. бюджет", 
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]
    )
    budget_max = models.DecimalField(
        "Макс. бюджет", 
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]
    )
    region = models.CharField("Регион поставки", max_length=100)
    deadline = models.DateField("Срок подачи предложений")
    status = models.CharField(
        "Статус", 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active'
    )
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)
    is_urgent = models.BooleanField("Срочный", default=False)
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-is_urgent", "-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["buyer", "created_at"]),
            models.Index(fields=["category", "status"]),
        ]

    def __str__(self):
        return f"#{self.id} {self.title}"
    
    def clean(self):
        if self.deadline <= timezone.now().date():
            raise ValidationError({"deadline": "Срок должен быть в будущем"})
        
        if self.budget_min and self.budget_max:
            if self.budget_min > self.budget_max:
                raise ValidationError({
                    "budget_min": "Минимум не может быть больше максимума",
                    "budget_max": "Максимум должен быть больше минимума"
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Offer(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="offers",
        verbose_name="Заказ"
    )
    supplier = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="offers",
        verbose_name="Поставщик"
    )
    price = models.DecimalField(
        "Цена", 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    delivery_days = models.PositiveIntegerField(
        "Срок поставки (дни)",
        validators=[MinValueValidator(1)]
    )
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    is_selected = models.BooleanField("Выбрано", default=False)
    
    class Meta:
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"
        unique_together = ['order', 'supplier']
        ordering = ["price", "delivery_days"]

    def __str__(self):
        return f"Предложение #{self.id} к заказу #{self.order.id}"
    
    def save(self, *args, **kwargs):
        if self.order.status != 'active':
            raise ValidationError("Можно создавать предложения только к активным заказам")
        super().save(*args, **kwargs)

class Message(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='messages',
        verbose_name="Заказ"
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Отправитель"
    )
    content = models.TextField("Сообщение")
    timestamp = models.DateTimeField("Время", auto_now_add=True)
    is_read = models.BooleanField("Прочитано", default=False)
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=["order", "timestamp"]),
        ]

    def __str__(self):
        return f"Сообщение #{self.id} в заказе #{self.order.id}"
