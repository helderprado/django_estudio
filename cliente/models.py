from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Clientes(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	data = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	nome = models.CharField(max_length=200, unique=True)
	telefone = models.CharField(max_length=200, null=True, blank=True)
	endereco = models.CharField(max_length=200, null=True, blank=True)

	class Meta:
		ordering = ['nome',]

	def __str__(self):
		return str(self.user)



		


