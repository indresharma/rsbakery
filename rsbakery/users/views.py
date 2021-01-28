from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model, login
from django.views.generic import View, UpdateView, DetailView, TemplateView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .forms import RegisterForm, ProfileForm
from .models import Profile
from .tokens import account_activation_token

class OwnerOnlyMixin:
    """Authorize only the owner of the object to update or delete an item"""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Unauthorized', status=401)

class RegisterView(View):
    """To register a new user with email-verification"""
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.profile.first_name = first_name
            user.profile.last_name = last_name
            user.save()
            # registraion via email verification
            current_site = get_current_site(request)
            email_subject = "Please complete you registration"
            message = render_to_string('users/user_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            messages.success(request, 'Activation link sent you your email ID. Please check you inbox')
            return redirect('users:login')
        # messages.error(request, 'Sorry username already taken')
        return render(request, 'users/register.html', {'form': form})

def activate_account(request, uidb64, token):
    """To activate the user profile after validating the token"""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().ObjectDoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your account has been activated successfully!")
        return redirect('users:profile')
    
    messages.error(request, 'Activation link is invalid!')
    return redirect('users:register')


class ProfileView(LoginRequiredMixin, TemplateView):
    """To display the User Profile"""
    # model = Profile
    template_name = 'users/profile.html'


class ProfileUpdate(LoginRequiredMixin, OwnerOnlyMixin, UpdateView):
    """To update the user profile"""
    model = Profile
    # fields = ('first_name', 'last_name', 'image', 'location', 'about_me', 'phone')
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')






