from django import template


register = template.Library()


@register.filter
def plus_years(obj, yrs):
    return obj.plus(yrs)
