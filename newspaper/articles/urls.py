from django.urls import path, re_path
from .views import ArticleListView, ArticleUpdateView, ArticleDetailView,  ArticleDeleteView, ArticleCreateView, UserLoginView, UserLogoutView, UserRegistrationView, activate, change_password

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:pk>/edit/',
         ArticleUpdateView.as_view(), name='article_edit'),  # new
    path('<int:pk>/',
         ArticleDetailView.as_view(), name='article_detail'),  # new
    path('<int:pk>/delete/',
         ArticleDeleteView.as_view(), name='article_delete'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    re_path(r'^login/$', UserLoginView, name="user-login"),
    re_path('logout/', UserLogoutView, name="user-logout"),


    re_path(r'^register/$', UserRegistrationView, name="user-registration"),

    path('activate/<slug:uidb64>/<slug:token>/',
         activate, name='user-activate'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),


    path('change_password', change_password, name="change_password"),

]
