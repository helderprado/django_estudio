from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from estoque.views import *

urlpatterns = [
	#páginas dos clientes
	path('cliente/', cliente_view , name='cliente'),
	path('cadastrar_cliente/', cadastro_cliente_view , name='cadastrar_cliente'),


	#páginas da administração
	path('cliente_admin/<list_id>', cliente_admin_view , name='cliente_admin'),
	path('base_clientes/', clientes_view , name='clientes'),
	path('cadastros/', cadastros_view , name='cadastros'),
	path('registro/', registro_view , name='registro'),
	path('login/', login_view , name='login'),
	path('logout/', logoutUser , name='logout'),
	path('cadastrar_cliente/', cadastro_cliente_view , name='cadastrar_cliente'),
	path('cadastrar_pedido/', cadastro_pedido_view , name='cadastrar_pedido'),
	path('pedidos_ativos/', pedidos_ativos_view , name='pedidos_ativos'),
	path('pedidos/', pedidos_view , name='pedidos'),
	path('ver_etiquetada/<pedido_id>/<item_id>', ver_etiquetada , name='ver_etiquetada'),
	path('ver_estampada/<pedido_id>/<item_id>', ver_estampada , name='ver_estampada'),
	path('ver_pronta_entrega/<pedido_id>/<item_id>', ver_pronta_entrega , name='ver_pronta_entrega'),
	path('ver_entrega/<pedido_id>/<item_id>', ver_entrega , name='ver_entrega'),
	path('pedido/<list_id>', pedido_view , name='pedido'),
	path('retirar_estoque/', retirar_estoque_view , name='retirar_estoque'),
	path('adicionar_estoque/', adicionar_estoque_view , name='adicionar_estoque'),
	path('estoque/', estoque_view , name='estoque'),
	path('deletar_produto/<list_id>', deletar_produto , name='deletar_produto'),
    path('editar_produto/<list_id>', editar_produto_view, name='editar_produto'),

    path('reset_password/', 
    	auth_views.PasswordResetView.as_view(template_name="password_reset.html"), 
    	name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='passord_reset_complete'),
]