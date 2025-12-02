# apps/subscriptions/models.py
from django.db import models
from django.utils import timezone
from apps.users.models import User

class SubscriptionPlan(models.Model):
    """Тарифные планы с кредитами для покупки контактов"""
    
    name = models.CharField("Название тарифа", max_length=100)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена (₽)", max_digits=10, decimal_places=2)
    contact_credits = models.PositiveIntegerField("Кредитов на контакты")
    duration_days = models.PositiveIntegerField("Срок (дней)")
    max_contacts_per_day = models.PositiveIntegerField("Макс контактов в день", default=100)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Тарифный план"
        verbose_name_plural = "Тарифные планы"
        ordering = ['price']

    def __str__(self):
        return f"{self.name} ({self.contact_credits} контактов)"


class UserSubscription(models.Model):
    """Активная подписка пользователя"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name="Пользователь"
    )
    
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        verbose_name="Тариф"
    )
    
    remaining_credits = models.PositiveIntegerField("Осталось кредитов")
    activated_at = models.DateTimeField("Активирована", auto_now_add=True)
    expires_at = models.DateTimeField("Истекает")
    contacts_purchased = models.PositiveIntegerField("Куплено контактов", default=0)

    class Meta:
        verbose_name = "Подписка пользователя"
        verbose_name_plural = "Подписки пользователей"

    def __str__(self):
        return f"{self.user.email} → {self.plan.name}"

    def is_active(self):
        """Проверяет, активна ли подписка"""
        return self.expires_at > timezone.now() and self.remaining_credits > 0
    
    def can_purchase_contact(self, contact_price=1):
        """Может ли купить контакт за X кредитов"""
        return self.is_active() and self.remaining_credits >= contact_price
