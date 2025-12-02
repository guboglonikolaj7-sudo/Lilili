# backend/apps/suppliers/models_contact.py
from django.db import models
from django.core.exceptions import ValidationError
import re

class SupplierContact(models.Model):
    """
    Контакт поставщика (платная информация)
    Каждый контакт (WhatsApp, Telegram и т.д.) продается отдельно
    """
    
    MESSENGER_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('vk', 'ВКонтакте'),
        ('wechat', 'WeChat'),
        ('phone', 'Телефон'),
        ('email', 'Email'),
    ]
    
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name="Поставщик"
    )
    
    contact_type = models.CharField(
        "Тип контакта",
        max_length=20,
        choices=MESSENGER_CHOICES,
        db_index=True
    )
    
    value = models.CharField(
        "Значение контакта",
        max_length=255,
        help_text="Номер, email, username, ID"
    )
    
    is_verified = models.BooleanField(
        "Контакт проверен модератором",
        default=False,
        db_index=True,
        help_text="Только проверенные контакты можно купить"
    )
    
    verification_date = models.DateTimeField(
        "Дата проверки",
        null=True,
        blank=True
    )
    
    added_at = models.DateTimeField(
        "Добавлен в базу",
        auto_now_add=True,
        db_index=True
    )
    
    # Цена может отличаться (WhatsApp дороже email)
    price_credits = models.PositiveIntegerField(
        "Стоимость в кредитах",
        default=1,
        help_text="Сколько кредитов снимется за покупку"
    )
    
    # Статистика
    times_purchased = models.PositiveIntegerField(
        "Сколько раз купили",
        default=0
    )
    
    last_purchased_at = models.DateTimeField(
        "Последняя покупка",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Контакт поставщика"
        verbose_name_plural = "Контакты поставщиков"
        unique_together = ('supplier', 'contact_type', 'value')
        ordering = ['-is_verified', 'contact_type']
        indexes = [
            models.Index(fields=['supplier', 'contact_type']),
            models.Index(fields=['is_verified', 'price_credits']),
        ]

    def __str__(self):
        return f"{self.supplier.name} | {self.get_contact_type_display()}: {self.masked_value()}"

    def clean(self):
        """Валидация формата контакта"""
        if self.is_verified:  # Валидация только для проверенных
            if self.contact_type == 'phone':
                self._validate_phone()
            elif self.contact_type == 'whatsapp':
                self._validate_whatsapp()
            elif self.contact_type == 'telegram':
                self._validate_telegram()
            elif self.contact_type == 'vk':
                self._validate_vk()
            elif self.contact_type == 'email':
                self._validate_email()

    def _validate_phone(self):
        pattern = r'^\+?\d{10,15}$'
        if not re.match(pattern, self.value.replace(' ', '').replace('-', '')):
            raise ValidationError('Телефон должен быть в формате +79161234567')

    def _validate_whatsapp(self):
        # WhatsApp использует тот же формат, что и телефон
        self._validate_phone()

    def _validate_telegram(self):
        pattern = r'^[a-zA-Z0-9_]{5,32}$'
        if not re.match(pattern, self.value.replace('@', '')):
            raise ValidationError('Telegram username должен быть 5-32 символа')

    def _validate_vk(self):
        pattern = r'^[a-zA-Z0-9_.]{5,32}$'
        if not re.match(pattern, self.value):
            raise ValidationError('VK ID/username невалиден')

    def _validate_email(self):
        from django.core.validators import validate_email
        validate_email(self.value)

    def masked_value(self):
        """Маскированное значение для предпросмотра (пока не купили)"""
        if self.contact_type in ['phone', 'whatsapp']:
            return self.value[:6] + '•' * (len(self.value) - 6)
        elif self.contact_type == 'email':
            parts = self.value.split('@')
            return parts[0][:2] + '•' * len(parts[0][2:]) + '@' + parts[1]
        elif self.contact_type == 'telegram':
            return '@' + self.value[:2] + '•' * len(self.value[2:])
        elif self.contact_type == 'vk':
            return 'vk.com/' + self.value[:2] + '•' * len(self.value[2:])
        return '•' * len(self.value)

    def get_direct_link(self):
        """Получить прямую ссылку для перехода"""
        if self.contact_type == 'whatsapp':
            clean_number = self.value.replace(' ', '').replace('-', '').replace('+', '')
            return f"https://wa.me/{clean_number}"
        elif self.contact_type == 'telegram':
            username = self.value.replace('@', '')
            return f"https://t.me/{username}"
        elif self.contact_type == 'vk':
            return f"https://vk.com/{self.value}"
        elif self.contact_type == 'wechat':
            # WeChat использует QR или ID
            return f"weixin://dl/chat?{self.value}"
        return None


class ContactAccess(models.Model):
    """
    История покупки доступа к контакту
    Каждый пользователь покупает каждый контакт 1 раз
    """
    
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='purchased_contacts',
        verbose_name="Покупатель",
        db_index=True
    )
    
    contact = models.ForeignKey(
        SupplierContact,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name="Контакт"
    )
    
    purchased_at = models.DateTimeField(
        "Дата и время покупки",
        auto_now_add=True,
        db_index=True
    )
    
    # Сколько реально списали (может отличаться от price_credits при акциях)
    credits_spent = models.PositiveIntegerField(
        "Потрачено кредитов",
        default=1
    )
    
    # Привязка к RFQ (опционально)
    # Это позволяет купить контакт прямо из закупки
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Закупка (RFQ)",
        help_text="Если контакт купили для конкретного RFQ"
    )
    
    # Метод оплаты: кредиты, реферальные бонусы и т.д.
    payment_method = models.CharField(
        "Способ оплаты",
        max_length=20,
        choices=[
            ('credits', 'Кредиты подписки'),
            ('referral', 'Реферальные бонусы'),
            ('promo', 'Промокод'),
        ],
        default='credits'
    )

    class Meta:
        verbose_name = "Доступ к контакту"
        verbose_name_plural = "Доступы к контактам"
        unique_together = ('user', 'contact')  # Нельзя купить дважды
        ordering = ['-purchased_at']
        indexes = [
            models.Index(fields=['user', '-purchased_at']),
            models.Index(fields=['contact', '-purchased_at']),
        ]

    def __str__(self):
        return f"{self.user.email} → {self.contact.supplier.name}"

    def save(self, *args, **kwargs):
        # Атомарное обновление статистики контакта
        if not self.pk:  # Только при создании
            SupplierContact.objects.filter(pk=self.contact.pk).update(
                times_purchased=models.F('times_purchased') + 1,
                last_purchased_at=timezone.now()
            )
        super().save(*args, **kwargs)


# Не забудьте импорт вверху файла
from django.utils import timezone