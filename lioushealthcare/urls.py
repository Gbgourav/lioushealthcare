"""remiteazy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import home
    2. Add a URL to urlpatterns:  url(r'^$', home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import re_path, include
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'^accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    re_path(r'^vendor/', include(('vendor.urls', 'vendor'), namespace='vendor')),
    re_path(r'^doctor/', include(('doctor.urls', 'doctor'), namespace='doctor')),
    re_path(r'^pharmacy/', include(('pharmacy.urls', 'pharmacy'), namespace='pharmacy')),
    re_path(r'^blood_bank/', include(('blood_bank.urls', 'blood_bank'), namespace='blood_bank')),
    re_path(r'^labtest/', include(('labtests.urls', 'blood_bank'), namespace='labtests')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
