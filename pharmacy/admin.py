from django.contrib import admin

from pharmacy.models import *

admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(ProductBrand)
admin.site.register(ProductRating)
admin.site.register(ProductOffer)
admin.site.register(Products)
admin.site.register(HealthConcerns)
admin.site.register(ProductReview)
admin.site.register(Cart)
admin.site.register(Order)
