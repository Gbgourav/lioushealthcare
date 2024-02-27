# payment/models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

UserAccount = get_user_model()


class Payment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user} - ${self.amount} - {self.payment_date}"
