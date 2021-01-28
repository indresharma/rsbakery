from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from PIL import Image
from django.core.files import File
from .models import Profile

class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    # To make name fields required
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password1'].help_text = None


class ProfileForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'about_me', 'location', 'phone', 'image', 'x', 'y', 'width', 'height', )

    def save(self):
        profile = super(ProfileForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        img = Image.open(profile.image)
        cropped_image = img.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(profile.image.path)

        return profile