from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    is_active = models.BooleanField("Активна", default=False)
    expires_at = models.DateTimeField("Действует до", null=True, blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {'активна' if self.is_active else 'не активна'}"