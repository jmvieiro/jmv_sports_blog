from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Row, Field, Layout, Div, Button
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from business_layer.models import *


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'subject'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('username', wrapper_class='col-xl-12 p-3',
                          css_class='form-control'),
                ),
                Row(
                    Field('password', wrapper_class='col-xl-12 p-3',
                          css_class='form-control'),
                ),
                css_class='form-group'),
            Div(
                Submit('submit', 'Iniciá sesión',
                       css_class='text-uppercase center btn btn-info btn-sm'),
                css_class='col-12'),
        )


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True, label="Usuario")
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True, label="Nombre")
    last_name = forms.CharField(
        max_length=100, required=True, label="Apellido")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'subject'
        self.helper.form_method = 'post'
        #self.helper.form_action = 'register'
        # self.helper.add_input(
        #     Submit('submit', 'Confirmar', css_class='text-uppercase center btn btn-info btn-sm col-xs-12'))
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('username', wrapper_class='col-md-6 p-3',
                          css_class='form-control'),
                    Field('email', wrapper_class='col-md-6 p-3',
                          css_class='form-control'),
                ),
                Row(
                    Field('first_name', wrapper_class='col-md-6 p-3',
                          css_class='form-control'),
                    Field('last_name', wrapper_class='col-md-6 p-3',
                          css_class='form-control'),
                ),
                Row(
                    Field('password1', wrapper_class='col-md-6 p-3',
                          css_class='form-control'),
                    Field('password2', wrapper_class='col-md-6 p-3',
                          css_class='form-control'),
                ),
                css_class='form-group'),
            Div(
                Submit('submit', 'Confirmar',
                       css_class='text-uppercase center btn btn-info btn-sm'),
                css_class='col-12'),
        )


class CommentForm(forms.Form):
    text = forms.CharField(max_length=300, label="Comentario")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', 'Confirmar', css_class='center btn-sm btn-default'))
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('text', wrapper_class='col-12',
                          css_class='form-control'),
                ),
                css_class='form-group'),
        )


class AvatarForm(forms.Form):
    avatar = forms.ImageField(label="Avatar")
