from django import template

register = template.Library()


@register.filter(name='zip_two')
def zip_lists_two(a, b):
    return zip(a, b)

@register.filter(name='zip_three')
def zip_lists_three(a, b):
    list_1 = b[0]
    list_2 = b[1]
    return zip(a, list_1, list_2)

@ register.filter(name='times')
def times (count) : 
    return range (int (count))