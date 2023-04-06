from django.urls import path
from .views import *

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', ArticleListView, name='article_list'),
    path('<int:pk>/edit/',
         ArticleUpdateView.as_view(), name='article_edit'),
    path('<slug:title>/',
         ArticleDetailView, name='article_detail'),
    path('<int:pk>/delete/',
         ArticleDeleteView.as_view(), name='article_delete'),
    path('new', ArticleCreateView.as_view(), name='article_new'),
    path('login', UserLoginView, name="user-login"),
    path('logout', UserLogoutView, name="user-logout"),
    path('register', UserRegistrationView, name="user-registration"),
    path('activate/<slug:uidb64>/<slug:token>/',
         activate, name='user-activate'),
    path("<slug:title>/comment/new", new_comment, name="new_comment"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('change_password', change_password, name="change_password"),
    path("like-article", like_article, name="like_article"),
    path("dislike-article", dislike_article, name="dislike_article"),




]
