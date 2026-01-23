from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('logo-icon.svg'), permanent=True), name='favicon'),
    path('', include('employees.urls')),
    path('employees/', include('employees.urls')),
]
