from django.db import models
from django.contrib.auth import get_user_model
from apps.suppliers.models import Category

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Завершен'), 
        ('cancelled', 'Отменен'),
    ]
    
    title = models.CharField("Название заказа", max_length=200)
    description = models.TextField("Описание")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    budget_min = models.DecimalField("Мин. бюджет", max_digits=12, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField("Макс. бюджет", max_digits=12, decimal_places=2, null=True, blank=True)
    region = models.CharField("Регион поставки", max_length=100)
    deadline = models.DateField("Срок подачи предложений")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    
    def __str__(self):
        return self.title

class Offer(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="offers")
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2)
    delivery_days = models.PositiveIntegerField("Срок поставки (дни)")
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    
    class Meta:
        unique_together = ['order', 'supplier']
    
    def __str__(self):
        return f"Предложение от {self.supplier.email} к заказу {self.order.title}"


class Message(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Сообщение от {self.sender.email} в заказе {self.order.id}"