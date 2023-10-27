from women.views import *
from django.urls import path, include
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', WomenHome.as_view(), name="home"),
    path('about/', about, name="about"),
    path('add-article/', AddArticle.as_view(), name="add-article"),
    path('contact/', ContactFormView.as_view(), name="contact"),
    path('sign-in/', SignInUser.as_view(), name="sign-in"),
    path('sign-up/', SignUpUser.as_view(), name="sign-up"),
    path('logout/', logout_user, name="logout"),
    path('article/<slug:article_slug>/', ShowArticle.as_view(), name="read-article"),
    path('category/<slug:category_slug>', WomenCategory.as_view(), name="show-women-by-category"),

    path('categories/<int:categories_id>/', category),
    path('check/', check_get)
]