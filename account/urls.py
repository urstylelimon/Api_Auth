from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.user_registration,name = 'user_registration'),
    path('login/',views.UserLoginView,name = 'login'),
    path('profile/',views.UserView,name = 'profile'),
    path('changepassword/',views.ChangePassword,name = 'changepassword'),
    path('passwordreset/',views.PasswordReset,name = 'passwordreset'),
    path('reset/<uid>/<token>/',views.UserPasswordResetView,name='reset'),
    
]
