from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from users import views as user_views


app_name = 'users'


urlpatterns = [
    path('register/', user_views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    path('profile-update/<int:pk>/',
         user_views.ProfileUpdate.as_view(), name='update_profile'),
    path('activate/<uidb64>/<token>/',
         user_views.activate_account, name='activate'),
    path('password-change/', user_views.UserPasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name="password_change_done"),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        success_url=reverse_lazy('users:password_reset_done'),
        email_template_name='users/password_reset_email.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),

    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
