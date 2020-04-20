from django import template

register = template.Library()

@register.filter
def estampada(pedido):
    return pedido.filter(estampada=True).count()