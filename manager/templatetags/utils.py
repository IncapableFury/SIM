from django import template

register = template.Library()

@register.filter
def add(value, arg):
    return "{:.2f}".format(float(value + arg))