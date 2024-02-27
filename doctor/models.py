from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

UserAccount = get_user_model()


class DoctorType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
