from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='users/password_change_form.html'
        ),
        name='PasswordChangeForm'
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='PasswordChangeDone'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset_form.html'
        ),
        name='PasswordReset'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='PasswordResetDone'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='PasswordResetComplete'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='PasswordResetConfirm'
    ),
    path(
        'signup/',
        views.SignUp.as_view(),
        name='signup'
    ),
]
