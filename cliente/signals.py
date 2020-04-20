from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Clientes


@receiver(post_save, sender=User)
def criar_cliente(sender, instance, created, **kwargs):

	if created:
		group = Group.objects.get(name='clientes')
		instance.groups.add(group)
		Clientes.objects.create(user=instance, nome=instance.username)
		print('Cliente criado.')