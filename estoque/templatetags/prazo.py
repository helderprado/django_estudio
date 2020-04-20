from datetime import datetime
from django import template

register = template.Library()

@register.filter
def prazo(date):
    prazo = date - datetime.now().date()
    return prazo.days