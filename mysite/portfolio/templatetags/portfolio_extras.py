from django import template

register = template.Library()

@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return ''

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg