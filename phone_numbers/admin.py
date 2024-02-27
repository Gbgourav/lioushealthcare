from django.contrib import admin
from .models import PhoneNumber

# Register your models here.


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('uid', 'contact_no', 'created_at')


admin.site.register(PhoneNumber, PhoneNumberAdmin)