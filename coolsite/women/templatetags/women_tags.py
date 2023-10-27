from django import template
from women.models import *

register = template.Library()


@register.simple_tag(name="get_cat")
def get_categories():
    return Category.objects.all()


@register.simple_tag(name="get_women")
def get_women(sort=None):
    if not sort:
        return Women.objects.all()
    else:
        return Women.objects.order_by(sort)


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, category_selected=0):
    if not sort:
        categories = Category.objects.all()
    else:
        categories = Category.objects.order_by(sort)
    return {"categories": categories, "category_selected": category_selected}