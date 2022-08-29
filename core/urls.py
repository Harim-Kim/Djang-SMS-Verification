from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_core, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html')),
    path('verify_code/', views.verify_code, name='verify'),
    path('reverify/', views.reverify),
    path('phone_verify/', views.phone_verify),
    path('signup_phone_verify_page/', views.signup_phone_verify_page, name='pre_signup_phone_verify'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('change_password/', views.change_password, name='change_password')
]
