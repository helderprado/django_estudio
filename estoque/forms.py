from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models	import User
from django import forms

from .models import *
from cliente.models import *

class AdicionarItemEstoque(forms.ModelForm):

	class Meta:
		model = Estoque
		fields = '__all__'

class AdicionarCor(forms.ModelForm):

	class Meta:
		model = Cores
		fields = '__all__'

class AdicionarTipos(forms.ModelForm):

	class Meta:
		model = Tipos
		fields = '__all__'

class AdicionarItensPedido(forms.ModelForm):

	class Meta:
		model = ItensPedido
		fields = [
			'pedido',
			'tipo',
			'cor',
			'tamanho',
			'estampa'
		]

class DateInput(forms.DateInput):
	input_type = 'date'

class CadastrarPedido(forms.ModelForm):

	class Meta:
		model = Pedidos
		fields = '__all__'
		widgets = {
            'prazo': DateInput(), # specify date-frmat
        }

class CadastrarCliente(forms.ModelForm):

	class Meta:
		model = Clientes
		fields = '__all__'
		exclude = ['user']

class CriarUsuario(UserCreationForm):

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2'
		]



