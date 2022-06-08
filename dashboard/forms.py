from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Row, Field, Layout, Div, Button
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from business_layer.models import *


class UserEditForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label="Nombre")
    last_name = forms.CharField(
        max_length=100, required=True, label="Apellido")
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput, label="Modificar contraseña")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'subject'
        self.helper.form_method = 'post'
        self.helper.form_action = 'dashboard:user_form'
        self.helper.add_input(
            Button('cancel', 'Cancelar', css_class='btn-secondary text-uppercase', onclick="window.location.href='/dashboard/user/index'"))
        self.helper.add_input(
            Submit('submit', 'Confirmar', css_class='text-uppercase'))
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('email', wrapper_class='col-xl-12 p-3',
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
        )


class SubjectForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(max_length=100, label="Nombre")
    is_active = forms.TypedChoiceField(
        label="Estado",
        choices=((True, "Activo"), (False, "Inactivo")),
        widget=forms.RadioSelect,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'subject'
        self.helper.form_method = 'post'
        self.helper.form_action = 'dashboard:subject_create_or_update'
        self.helper.add_input(
            Submit('submit', 'Confirmar', css_class='text-uppercase center'))
        self.helper.layout = Layout(
            Div(
                Row(Field('id')),
                Row(
                    Field('name', wrapper_class='col-md-6 p-3',
                          css_class='form-control'),
                    Field('is_active', wrapper_class='col-md-6 p-3',
                          css_class='form-check'),
                ),
                css_class='form-group'),
        )


class PostForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    title = forms.CharField(max_length=100, label="Título")
    subtitle = forms.CharField(max_length=200, label="Subtítulo")
    content = forms.CharField(widget=forms.Textarea, label="Contenido")
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_active=True), label="Tema")
    image = forms.ImageField(
        label="Imagen", required=False, widget=forms.FileInput)
    is_active = forms.TypedChoiceField(
        label="Estado",
        choices=((True, "Activo"), (False, "Inactivo")),
        widget=forms.RadioSelect,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'post'
        self.helper.form_method = 'post'
        self.helper.form_action = 'dashboard:post_create_or_update'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(
            Submit('submit', 'Confirmar', css_class='text-uppercase center'))
        self.helper.layout = Layout(
            Div(
                Row(Field('id')),
                Row(
                    Field('title', wrapper_class='col-md-6 p-3',
                          css_class='form-control'),
                    Field('subtitle', wrapper_class='col-md-6 p-3',
                          css_class='form-control'),
                ),
                Row(
                    Field('content', wrapper_class='col-12 p-3',
                          css_class='form-control'),
                ),
                Row(
                    Field('subject', wrapper_class='col-md-4 p-3',
                          css_class='form-control'),
                    Field('image', wrapper_class='col-md-4 p-3',
                          css_class='form-control'),
                    Field('is_active', wrapper_class='col-md-4 p-3',
                          css_class='form-check'),
                ),
                css_class='form-group'),
        )


class AvatarForm(forms.Form):

    user = forms.ModelChoiceField(
        queryset=User.objects.all(), label="Usuario")

    avatar = forms.ImageField(label="Avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'avatar'
        self.helper.form_method = 'post'
        self.helper.form_action = 'dashboard:user_edit_avatar'
        self.helper.add_input(
            Button('cancel', 'Cancelar', css_class='btn-secondary text-uppercase', onclick="window.location.href='/dashboard/user/form'"))
        self.helper.add_input(
            Submit('submit', 'Confirmar', css_class='text-uppercase'))
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('user', wrapper_class='col-xl-6 p-3',
                          css_class='form-control'),
                    Field('avatar', wrapper_class='col-xl-6 p-3',
                          css_class='form-control'),
                ),
                css_class='form-group'),
        )
