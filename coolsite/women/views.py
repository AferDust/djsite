from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy
from women.froms import *
from women.models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'women'

    # extra_context = {'title': 'Main Page'}  # only for static variables

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main Page')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('category')


# def index(request):
#     context = {
#         'title': 'Main Page',
#         "menu": menu,
#         "category_selected": 0,
#     }
#     return render(request, 'women/index.html', context=context)


class ShowArticle(DataMixin, DetailView):
    model = Women
    template_name = 'women/show_article.html'
    slug_url_kwarg = 'article_slug'
    # pk_url_kwarg =
    context_object_name = 'women'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['women'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_article(request, article_slug):
#     article = get_object_or_404(Women, slug=article_slug)
#     context = {
#         "menu": menu,
#         "women": article,
#         "category_selected": article.category_id,
#     }
#
#     return render(request, 'women/show_article.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'title': 'About Page', 'menu': menu, "category_selected": 0})


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/show_women_by_category.html'
    context_object_name = 'women'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title="Category - " + str(c.name),
                                      category_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True).select_related('category')


# def show_women_by_category(request, category_slug):
#     for_take_category_id = Category.objects.get(slug=category_slug)
#     women_by_category = Women.objects.filter(category=for_take_category_id.pk)
#
#     if not women_by_category:
#         raise Http404()
#
#     context = {
#         "menu": menu,
#         "women": women_by_category,
#         "category_selected": for_take_category_id.pk,
#     }
#
#     return render(request, 'women/show_women_by_category.html', context=context)


class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddArticleForm
    template_name = 'women/add_article.html'
    success_url = reverse_lazy('home')
    # login_url = reverse_lazy('sing-in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Adding Article")
        return dict(list(context.items()) + list(c_def.items()))


# def add_article(request):
#     if request.method == 'POST':
#         form = AddArticleForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddArticleForm()
#
#     context = {
#         "menu": menu,
#         "form": form,
#         "title": "Add article"
#     }
#
#     return render(request, 'women/add_article.html', context=context)


class SignUpUser(DataMixin, CreateView):
    form_class = SignUpUserForm
    template_name = 'women/sign_up.html'
    # success_url = reverse_lazy('sign-in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign Up')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class SignInUser(DataMixin, LoginView):
    form_class = SignInUserForm
    template_name = 'women/sign_in.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign In')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('sign-in')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    # success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Feedback')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def sign_in(request):
#     return HttpResponse("Login page")


def category(request, categories_id):
    return HttpResponse(f"<h1>Categories of women</h1><p>{categories_id}</p>")


def check_get(request):
    if request.GET:
        name = request.GET.get('name')
        if name == "Dias":
            return redirect('home', permanent=True)
        else:
            return HttpResponse(request.GET.get('name') + " " + request.GET.get('type'))
    else:
        return HttpResponse("<h1>No get information</h1>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page Not Found.</h1>")
