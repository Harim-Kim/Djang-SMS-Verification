from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html')),
    path('verify/', views.verify_code),
    path('reverify/', views.reverify),
    path('phone_verify/', views.phone_verify),
    path('signup_phone_verify_page/', views.signup_phone_verify_page),
]
