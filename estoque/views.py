
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from .decorators import *

from cliente.models import *

from .models import *

from .forms import *

# Create your views here.

#=======================================================================================
@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def estoque_view(request):

	estoque = Estoque.objects.all()
	filtro = estoque.order_by('tipo').values('tipo', 'cor').distinct()
	filtro_list = list(filtro)
	resultado = []


	for i in range(len(filtro_list)):

		entrada_MBL = estoque.filter(movimentacao="Entrada").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('MBL'))
		entrada_GBL = estoque.filter(movimentacao="Entrada").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('GBL'))
		entrada_P = estoque.filter(movimentacao="Entrada").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('P'))
		entrada_M = estoque.filter(movimentacao="Entrada").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('M'))
		entrada_G = estoque.filter(movimentacao="Entrada").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('G'))
		entrada_GG = estoque.filter(movimentacao="Entrada").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('GG'))

		saida_MBL = estoque.filter(movimentacao="Saida").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('MBL'))
		saida_GBL = estoque.filter(movimentacao="Saida").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('GBL'))
		saida_P = estoque.filter(movimentacao="Saida").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('P'))
		saida_M = estoque.filter(movimentacao="Saida").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('M'))
		saida_G = estoque.filter(movimentacao="Saida").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('G'))
		saida_GG = estoque.filter(movimentacao="Saida").filter(tipo=filtro_list[i]['tipo'], cor=filtro_list[i]['cor']).aggregate(Sum('GG'))

		default = 0

		resultado.append(filtro_list[i])
		resultado[i]['MBL'] = (entrada_MBL['MBL__sum'] or default) - (saida_MBL['MBL__sum'] or default)
		resultado[i]['GBL'] = (entrada_GBL['GBL__sum'] or default) - (saida_GBL['GBL__sum'] or default)
		resultado[i]['P'] = (entrada_P['P__sum'] or default) - (saida_P['P__sum'] or default)
		resultado[i]['M'] = (entrada_M['M__sum'] or default) - (saida_M['M__sum'] or default)
		resultado[i]['G'] = (entrada_G['G__sum'] or default) - (saida_G['G__sum'] or default)
		resultado[i]['GG'] = (entrada_GG['GG__sum'] or default) - (saida_GG['GG__sum'] or default)
	
	context = {

		'resultado': resultado

	}

	return render(request, 'estoque.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def adicionar_estoque_view(request):

	form = AdicionarItemEstoque(request.POST or None)
	form.fields["movimentacao"].initial = "Entrada"

	if form.is_valid():
		form.save()
		return redirect('adicionar_estoque')

	estoque = Estoque.objects.all()

	context = {
		'estoque': estoque,
		'form': form

	}

	return render(request, 'adicionar_estoque.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def retirar_estoque_view(request):

	form = AdicionarItemEstoque(request.POST or None)
	form.fields["movimentacao"].initial = "Saida"

	if form.is_valid():
		form.save()
		return redirect('retirar_estoque')

	estoque = Estoque.objects.all()

	context = {
		'estoque': estoque,
		'form': form

	}

	return render(request, 'retirar_estoque.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def editar_produto_view(request, list_id):

	item = Estoque.objects.get(pk=list_id)
	form = AdicionarItemEstoque(request.POST or None, instance=item)
	context = {
		'item': item,
		'form': form
	}

	if form.is_valid():
		form.save()
		return redirect('adicionar_estoque')

	else:
		return render(request, 'editar_produto.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def deletar_produto(request, list_id):

	item = Estoque.objects.get(pk=list_id)
	item.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#========================================================================================

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def pedido_view(request,list_id):

	form = AdicionarItensPedido(request.POST or None)
	pedido = Pedidos.objects.get(pk=list_id)

	form.fields["pedido"].initial = pedido.id

	if form.is_valid():
		form.save()
		return redirect('pedido', list_id = list_id)


	lista_itens = pedido.itenspedido_set.all()

	qnt_total = lista_itens.count()
	qnt_etiquetada = lista_itens.filter(etiquetagem=True).count()
	qnt_estampada = lista_itens.filter(estampada=True).count()
	qnt_pronta_entrega = lista_itens.filter(pronta_entrega=True).count()

	context = {

		'form': form,
		'pedido': pedido,
		'lista_itens': lista_itens,
		'qnt_etiquetada': qnt_etiquetada,
		'qnt_estampada': qnt_estampada,
		'qnt_pronta_entrega': qnt_pronta_entrega,
		'qnt_total': qnt_total,

	}

	return render(request, 'pedido.html', context)


#=========================================================================================

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def pedidos_view(request):

	pedidos = Pedidos.objects.all()

	quantidade_pedidos = pedidos.count()

	context = {

		'pedidos': pedidos,
		'quantidade_pedidos': quantidade_pedidos

	}

	return render(request, 'pedidos.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def pedidos_ativos_view(request):

	pedidos = Pedidos.objects.all()
	pedidos_ativos = pedidos.filter(status="Ativo")

	valores_acordados = pedidos_ativos.aggregate(Sum('valor_acordado'))
	soma_valores_acordados = valores_acordados['valor_acordado__sum']

	valores_pagos = pedidos_ativos.aggregate(Sum('valor_pago'))
	soma_valores_pagos = valores_pagos['valor_pago__sum']

	quantidade_ativos = pedidos_ativos.count()

	contagem = 0

	for pedido in pedidos_ativos:	
		contagem += pedido.itenspedido_set.all().count()


	context = {

		'pedidos': pedidos,
		'pedidos_ativos': pedidos_ativos,
		'quantidade_ativos': quantidade_ativos,
		'soma_valores_acordados': soma_valores_acordados,
		'soma_valores_pagos': soma_valores_pagos,
		'contagem': contagem

	}

	return render(request, 'pedidos_ativos.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def ver_etiquetada(request, pedido_id, item_id):

	item = Pedidos.objects.get(pk=pedido_id).itenspedido_set.get(pk=item_id)

	item.etiquetagem = not item.etiquetagem

	item.save()

	return redirect('pedido', list_id = pedido_id)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def ver_estampada(request, pedido_id, item_id):

	item = Pedidos.objects.get(pk=pedido_id).itenspedido_set.get(pk=item_id)

	item.estampada = not item.estampada

	item.save()

	return redirect('pedido', list_id = pedido_id)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def ver_pronta_entrega(request, pedido_id, item_id):

	item = Pedidos.objects.get(pk=pedido_id).itenspedido_set.get(pk=item_id)

	item.pronta_entrega = not item.pronta_entrega

	item.save()

	return redirect('pedido', list_id = pedido_id)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def ver_entrega(request, pedido_id, item_id):

	item = Pedidos.objects.get(pk=pedido_id).itenspedido_set.get(pk=item_id)

	item.entregue = not item.entregue

	item.save()

	if item.entregue == True:

	    pedido = Pedidos.objects.get(id=pedido_id)
	    item = pedido.itenspedido_set.filter(id=item_id).values()
	    item = item[0]
	    tipo = item['tipo_id']
	    cor = item['cor_id']
	    tamanho = str(item['tamanho'])

	    baixa = Estoque.objects.create(tipo_id=tipo, cor_id=cor, movimentacao="Saida")
	    setattr(baixa, tamanho, 1)
	    baixa.save()

	return redirect('pedido', list_id = pedido_id)


#=======================================================================================
@login_required(login_url='login')
@allowed_users(allowed_roles=['clientes','admin'])
def cadastro_pedido_view(request):

	form = CadastrarPedido(request.POST or None)
	
	context = {
		'form': form
	}

	if form.is_valid():
		form.save()	
		pedido = Pedidos.objects.latest('id')
		pk = pedido.id
		return redirect('pedido', list_id = pk)

	else:
		return render(request, 'cadastrar_pedido.html', context)

	return render(request, 'cadastrar_pedido.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['clientes','admin'])
def cadastro_cliente_view(request):

	cliente = request.user.clientes
	form = CadastrarCliente(instance=cliente)

	context = {
		'form': form
	}
	
	if request.method == 'POST':
		form = CadastrarCliente(request.POST, instance=cliente)
		if form.is_valid():
			form.save()	
			return redirect('cliente')

	else:
		return render(request, 'cadastrar_cliente.html', context)

	
	return render(request, 'cadastrar_cliente.html', context)


#====================================================================================

@unauthenticated_user
def registro_view(request):

	form = CriarUsuario()
	if request.method == 'POST':
		form = CriarUsuario(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, "Seu registro foi realizado com sucesso." + username)

			return redirect('login')

	context = {
		'form': form,

	}

	return render(request, 'registro.html', context)

@unauthenticated_user
def login_view(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('cliente')
		else:
			messages.info(request, "Você não tem um usuário")

	context = {}
	return render(request, 'login.html', context)


def logoutUser(request):
	logout(request)

	return redirect('login')

#=============================================================================

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def cadastros_view(request):

	form_cor = AdicionarCor()

	if request.method == 'POST':
		form_cor = AdicionarCor(request.POST)
		if form_cor.is_valid():
			form_cor.save()

	form_tipo = AdicionarTipos()

	if request.method == 'POST':
		form_tipo = AdicionarCor(request.POST)
		if form_tipo.is_valid():
			form_tipo.save()

	context = {
		'form_cor': form_cor,
		'form_tipo': form_tipo

	}

	return render(request, 'cadastros.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def clientes_view(request):

	base_clientes = Clientes.objects.all()

	context = {
		'base_clientes': base_clientes,

	}

	return render(request, 'base_clientes.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def cliente_admin_view(request, list_id):

	cliente = Clientes.objects.get(id=list_id)
	pedidos = cliente.pedidos_set.all()
	pedidos_ativos = cliente.pedidos_set.all().filter(status='Ativo').count()

	context = {
		'cliente': cliente,
		'pedidos': pedidos,
		'pedidos_ativos': pedidos_ativos

	}

	return render(request, 'cliente_admin.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','clientes'])
def cliente_view(request):

	cliente = request.user.clientes

	pedidos = request.user.clientes.pedidos_set.all()

	context = {
		'cliente': cliente,
		'pedidos': pedidos,

	}

	return render(request, 'cliente.html', context)

def user_view(request):
	pass










