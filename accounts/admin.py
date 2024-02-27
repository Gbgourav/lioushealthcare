from .models import UserAccount, UserLocation, State
from django.contrib import admin


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'contact_no')
    search_fields = ('first_name', 'last_name', 'email')


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(UserLocation)
admin.site.register(State)
