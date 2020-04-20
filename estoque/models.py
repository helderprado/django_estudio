from django.db import models

from cliente.models import Clientes

# Create your models here.

class Cores(models.Model):

	cor = models.CharField(max_length=200, unique=True)
	data = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	class Meta:
		ordering = ['cor',]

	def __str__(self):
		return self.cor

class Tipos(models.Model):

	tipo = models.CharField(max_length=200, unique=True)
	data = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	class Meta:
		ordering = ['tipo',]

	def __str__(self):
		return self.tipo


class Estoque(models.Model):

	tipo = models.ForeignKey(Tipos, to_field='tipo', on_delete= models.SET_NULL, null=True)
	cor = models.ForeignKey(Cores, to_field='cor', on_delete= models.SET_NULL, null=True)
	MBL = models.IntegerField(default=0)
	GBL = models.IntegerField(default=0)
	P = models.IntegerField(default=0)
	M = models.IntegerField(default=0)
	G = models.IntegerField(default=0)
	GG = models.IntegerField(default=0)
	movimentacao = models.CharField(max_length=200, default="Entrada")
	data = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	class Meta:
		ordering = ['-data',]

class Pedidos(models.Model):
	data = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	cliente = models.ForeignKey(Clientes, to_field='nome', on_delete= models.SET_NULL, null=True)
	valor_acordado = models.DecimalField(max_digits=1000, decimal_places=2)
	valor_pago = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
	status = models.CharField(default="Ativo", max_length = 100, blank=True, null=False)
	prazo = models.DateField(null=True, blank=True)

	class Meta:
		ordering = ['prazo',]

	def __str__(self):
		return self.cliente.nome


class ItensPedido(models.Model):

	TAMANHOS_CHOICES = (
			('MBL', 'MBL'),
			('GBL', 'GBL'),
			('P', 'P'),
			('M', 'M'),
			('G', 'G'),
			('GG', 'GG')
		)	

	pedido = models.ForeignKey(Pedidos, on_delete=models.PROTECT)
	tipo = models.ForeignKey(Tipos, to_field='tipo', on_delete= models.SET_NULL, null=True)
	cor = models.ForeignKey(Cores, to_field='cor', on_delete= models.SET_NULL, null=True)
	tamanho = models.CharField(max_length=200, default='', choices=TAMANHOS_CHOICES)
	estampa = models.CharField(max_length=200, null=True, blank=True)
	etiquetagem = models.BooleanField(default=False)
	estampada = models.BooleanField(default=False)
	entregue = models.BooleanField(default=False)
	pronta_entrega = models.BooleanField(default=False)
	observacoes = models.CharField(default="", max_length = 100, blank=True, null=False)

	def __str__(self):
		return self.pedido.cliente.nome + " | " + self.tipo.tipo




