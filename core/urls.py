from django.contrib import admin
from django.urls import path, include

from estoque import views

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('estoque.urls')),
    path('', include('cliente.urls')),
]
