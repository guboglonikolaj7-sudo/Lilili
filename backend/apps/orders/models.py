from django.db import models
from django.contrib.auth import get_user_model
from apps.suppliers.models import Supplier, Category

User = get_user_model()

class RFQ(models.Model):
    """Запрос на котировку от покупателя"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('closed', 'Закрыт'),
        ('cancelled', 'Отменен'),
    ]
    
    title = models.CharField("Название закупки", max_length=255)
    description = models.TextField("Техническое задание")
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория товара"
    )
    
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rfqs",
        verbose_name="Закупщик"
    )
    
    budget_min = models.DecimalField("Бюджет от", max_digits=12, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField("Бюджет до", max_digits=12, decimal_places=2, null=True, blank=True)
    
    deadline = models.DateTimeField("Срок подачи котировок")
    
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Запрос на котировку"
        verbose_name_plural = "Запросы на котировки"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.title} ({self.buyer.email})"


class Quote(models.Model):
    """Котировка от поставщика на RFQ"""
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('withdrawn', 'Отозвано'),
    ]
    
    rfq = models.ForeignKey(
        RFQ,
        on_delete=models.CASCADE,
        related_name="quotes",
        verbose_name="Закупка"
    )
    
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="quotes",
        verbose_name="Поставщик"
    )
    
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2)
    currency = models.CharField("Валюта", max_length=3, default="USD")
    
    delivery_time_days = models.PositiveIntegerField("Срок поставки (дни)")
    
    notes = models.TextField("Комментарий", blank=True)
    
    attachment = models.FileField(
        "Файл котировки",
        upload_to="quotes/%Y/%m/",
        blank=True
    )
    
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Котировка"
        verbose_name_plural = "Котировки"
        unique_together = ['rfq', 'supplier']  # Один поставщик = одна котировка на RFQ
    
    def __str__(self):
        return f"{self.supplier.name} → {self.rfq.title}: ${self.price}"


class Message(models.Model):
    """Сообщения для чата между покупателем и поставщиками"""
    SENDER_TYPES = [
        ('buyer', 'Закупщик'),
        ('supplier', 'Поставщик'),
        ('system', 'Система'),
    ]
    
    rfq = models.ForeignKey(
        RFQ,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Закупка"
    )
    
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Отправитель"
    )
    
    sender_type = models.CharField(
        "Тип отправителя",
        max_length=20,
        choices=SENDER_TYPES
    )
    
    content = models.TextField("Сообщение")
    
    attachment = models.FileField(
        "Вложение",
        upload_to="chat_files/%Y/%m/",
        blank=True
    )
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.email}: {self.content[:50]}"