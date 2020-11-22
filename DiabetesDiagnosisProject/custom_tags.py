from django import template
from .fetchData import main

register = template.Library()

@register.simple_tag
def loadRecord(pid):
    
    data = main("?id", "=", ":{}".format(pid))
    return data

@register.filter
def toString(value):

    return str(value)
