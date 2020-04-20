from django import template

register = template.Library()

@register.filter
def etiquetada(pedido):
    return pedido.filter(etiquetagem=True).count()