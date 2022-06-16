from django.urls import path 
from . import views

app_name = 'user'

urlpatterns = [
    path('user/register/', views.register_user, name="register-user"),
    path('user/login/', views.login_user, name="login-user"),
    path('user/logout/', views.logout_user, name="logout-user"),
    path('user/activate/<uidb64>/<token>/',views.activate_user, name="activate-user"),
    
]
