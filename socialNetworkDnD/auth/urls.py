
from django.urls import path
from django.contrib.auth import views as auth_views

from auth.views import UserCreateView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name="view")
]


