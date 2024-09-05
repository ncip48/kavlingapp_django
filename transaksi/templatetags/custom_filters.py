from django import template

register = template.Library()

@register.filter
def index_list(value, index):
    try:
        return value[index-1]
    except IndexError:
        return None