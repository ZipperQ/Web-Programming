from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Thing
from .models import Message
from django.contrib.auth.forms import UserChangeForm


class ThingForm(ModelForm):
    class Meta:
        model = Thing
        fields = ['name', 'category', 'address', 'contact', 'image', 'notes']
        labels = {
            'name': 'Название',
            'category': 'Категория',
            'address': 'Адрес',
            'contact': 'Контактная информация (цифры номера телефона необходимо вводить слитно для автоматического '
                       'приведения номера к шаблонному виду)',
            'image': 'Фотографии к вещи',
            'notes': 'Заметки (необязательно)'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'address-input'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone-input',
                                              'placeholder': 'X (XXX) XXX XX-XX'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': ''}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # Only text message
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите сообщение...',
                                             'rows': 8}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
