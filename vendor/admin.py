from django.contrib import admin

from blood_bank.models import BloodStock
from .models import *

# class DoctorVendorAdmin(admin.ModelAdmin):
#     list_display = ('establishment_name', 'address', 'contact', 'doctor_name', 'specialty', 'sub_specialty')
#
#
# class PathologyVendorAdmin(admin.ModelAdmin):
#     list_display = ('establishment_name', 'address', 'contact', 'days', 'timing')
#
#
# class PhlebologistVendorAdmin(admin.ModelAdmin):
#     list_display = ('establishment_name', 'address', 'contact', 'registration_no', 'motorcycle_reg_no')
#
#
# class PharmacyVendorVendorAdmin(admin.ModelAdmin):
#     list_display = ('establishment_name', 'address', 'contact', 'days', 'timing')


admin.site.register(DoctorVendor)
admin.site.register(PathologyVendor)
admin.site.register(PhlebologistVendor)
admin.site.register(PharmacyVendor)
admin.site.register(Slot)
admin.site.register(SlotTime)
admin.site.register(BookDoctorSlot)
admin.site.register(Review)
admin.site.register(Timing)
admin.site.register(Service)
admin.site.register(Specialization)
admin.site.register(BloodBankVendor)
admin.site.register(BloodStock)
admin.site.register(Facilities)
