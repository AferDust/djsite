from django.db.models import Count

from .models import *
from django.core.cache import cache

menu = [
    {'title': "About Site", 'url_name': "about"},
    {'title': "Add article", 'url_name': "add-article"},
    {'title': "Feedback", 'url_name': "contact"},
]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs

        categories = cache.get('categories')
        if not categories:
            categories = Category.objects.annotate(Count('women'))
            cache.set('categories', categories, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['categories'] = categories

        if 'category_selected' not in context:
            context['category_selected'] = 0

        return context
