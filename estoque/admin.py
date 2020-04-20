from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Estoque)
admin.site.register(Cores)
admin.site.register(Tipos)
admin.site.register(Pedidos)
admin.site.register(ItensPedido)
