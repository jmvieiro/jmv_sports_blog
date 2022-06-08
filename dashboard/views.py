from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError

# Create your views here.
from dashboard.forms import *
from business_layer.models import *
from business_layer.views import *


# logged in views - revisado

class AuthAdmin(LoginRequiredMixin, ListView):
    model = Post
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super(AuthAdmin, self).get_context_data(**kwargs)
        total = len(get_posts(is_active=True))
        publicados = 0
        noPublicados = 0
        try:
            delUsuario = Post.objects.filter(author=self.request.user)
            publicados = int(len(delUsuario.filter(is_active=True))/total*100)
            noPublicados = len(delUsuario.filter(is_active=False))
        except ZeroDivisionError:
            pass
        context['postsPublicados'] = total
        context['tusPostsPublicados'] = publicados
        context['tusPostsNoPublicados'] = noPublicados
        context['mensajesNoLeidos'] = len(Message.objects.filter(
            receiver=self.request.user, is_read=False))
        return context

# chat - revisado


@login_required
def chat_index(request, id=None):
    if id is None:
        return render(request, "chat/index.html", {"usuarios": User.objects.exclude(username=request.user), "destinatario": {}, "mensajes": []})
    try:
        destinatario = User.objects.get(pk=id)
        if destinatario == request.user:
            return render(request, "error.html", {"response": "El destinatario no puede ser el mismo que el emisor."})
    except User.DoesNotExist:
        return render(request, "error.html", {"response": "El destinatario o la conversación no existen.", "url": "/dashboard/chat/index"})
    except ValueError:
        return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero.", "url": "/dashboard/chat/index"})

    if request.method == "POST":
        mensaje = request.POST.get('message', None)
        if mensaje:
            Message.objects.create(sender=request.user,
                                   receiver=destinatario, content=mensaje)
        else:
            return render(request, "error.html", {"response": "El mensaje no puede estar vacío."})

    mensajes = Message.objects.filter(receiver=request.user, sender=id).__or__(
        Message.objects.filter(sender=request.user, receiver=id)).order_by('ts_created')
    for mensaje in mensajes:
        if mensaje.receiver == request.user:
            mensaje.is_read = True
            mensaje.save()
    return render(request, "chat/index.html", {"usuarios": User.objects.exclude(username=request.user), "destinatario": destinatario, "mensajes": mensajes})


# logged in - post views - revisado

class AuthPostIndex(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post/index.html"

    def get_context_data(self, **kwargs):
        context = super(AuthPostIndex, self).get_context_data(**kwargs)
        try:
            if self.request.user.is_superuser:
                context['posts'] = Post.objects.all()
            else:
                context['posts'] = Post.objects.filter(
                    author=self.request.user)
        except Post.DoesNotExist:
            context['posts'] = None
        return context


@login_required
def post_form(request, id=None):
    try:
        if id:  # update
            try:
                if request.user.is_superuser:
                    obj = Post.objects.get(id=id)
                else:
                    obj = Post.objects.get(id=id, author=request.user)
                form = PostForm(
                    initial={"id": obj.id, "title": obj.title, "subtitle": obj.subtitle, "content": obj.content, "image": obj.image, "is_active": obj.is_active, "subject": obj.subject})
                return render(request, "post/form.html", {"form": form, "url": obj.image.url})
            except Post.DoesNotExist:
                return render(request, "error.html", {"response": "El post no existe o no tenés permisos para visitarlo.", "url": "/dashboard/post/index"})
        else:  # create
            return render(request, "post/form.html", {"form": PostForm()})
    except ValueError:
        return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero."})


@login_required
def post_create_or_update(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.cleaned_data
        id = data.get("id")
        title = data.get("title")
        subtitle = data.get("subtitle")
        content = data.get("content")
        is_active = data.get("is_active")
        author = request.user

        subject = Subject.objects.get(id=data.get("subject").id)
        image = data.get("image")
        if (id is None):  # create
            obj = Post(title=title, subtitle=subtitle,
                       content=content, is_active=is_active, author=author, subject=subject, image=image)
            obj.save()
            return render(request, "success.html", {"response": "El post ha sido creado satisfactoriamente.", "url": "/dashboard/post/index"})
        else:  # update
            try:
                if request.user.is_superuser:
                    obj = Post.objects.get(id=id)
                else:
                    obj = Post.objects.get(id=id, author=request.user)
                obj.title = title
                obj.subtitle = subtitle
                obj.content = content
                obj.is_active = is_active
                obj.subject = subject
                if image:
                    if obj.image:
                        obj.image.delete()
                    obj.image = image
                obj.save()
                return render(request, "success.html", {"response": "El post ha sido actualizado satisfactoriamente.", "url": "/dashboard/post/index"})
            except Post.DoesNotExist:
                return render(request, "error.html", {"response": "El post no existe o no tenés permisos para modificarlo.", "url": "/dashboard/post/index"})
    else:
        return render(request, "error.html", {"response": "La página que estás intentando visitar no está disponible."})


@login_required
def post_update_state(request, id):
    try:
        if request.user.is_superuser:
            obj = Post.objects.get(id=id)
        else:
            obj = Post.objects.get(id=id, author=request.user)
        obj.is_active = not obj.is_active
        obj.save()
        return redirect("dashboard:post_index")
    except Post.DoesNotExist:
        return render(request, "error.html", {"response": "El post no existe o no tenés permisos para modificarlo.", "url": "/dashboard/post/index"})
    except ValueError:
        return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero.", "url": "/dashboard/post/index"})


@login_required
def post_delete(request, id):
    try:
        if request.user.is_superuser:
            obj = Post.objects.get(id=id)
        else:
            obj = Post.objects.get(id=id, author=request.user)
        return render(request, "post/delete.html", {"post": obj})
    except Post.DoesNotExist:
        return render(request, "error.html", {"response": "El post no existe o no tenés permisos para modificarlo.", "url": "/dashboard/post/index"})
    except ValueError:
        return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero.", "url": "/dashboard/post/index"})


@login_required
def post_delete_confirm(request, id):
    try:
        if request.user.is_superuser:
            obj = Post.objects.get(id=id)
        else:
            obj = Post.objects.get(id=id, author=request.user)
        obj.delete()
        return redirect("dashboard:post_index")
    except Post.DoesNotExist:
        return render(request, "error.html", {"response": "El post no existe o no tenés permisos para modificarlo.", "url": "/dashboard/post/index"})
    except ValueError:
        return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero.", "url": "/dashboard/post/index"})


# logged in - subject views - revisado

@login_required
@user_passes_test(lambda u: u.is_superuser)
def subject_index(request):
    return render(request, "subject/index.html", {"subjects": Subject.objects.all()})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def subject_form(request, id=None):
    try:
        if id:
            try:
                obj = Subject.objects.get(id=id)
                form = SubjectForm(
                    initial={"id": obj.id, "name": obj.name, "is_active": obj.is_active})
                return render(request, "subject/form.html", {"form": form})
            except Subject.DoesNotExist:
                return render(request, "error.html", {"response": "El tema no existe.", "url": "/dashboard/subject/index"})
        else:
            return render(request, "subject/form.html", {"form": SubjectForm()})
    except ValueError:
        return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero.", "url": "/dashboard/subject/index"})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def subject_create_or_update(request):
    form = SubjectForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        id = data.get("id")
        name = data.get("name")
        is_active = data.get("is_active")
        if (id is None):  # create
            obj = Subject(name=name, is_active=is_active)
            obj.save()
            return render(request, "success.html", {"response": "El tema ha sido creado satisfactoriamente.", "url": "/dashboard/subject/index"})
        else:  # update
            try:
                obj = Subject.objects.get(id=id)
                obj.name = name
                obj.is_active = is_active
                obj.save()
                return render(request, "success.html", {"response": "El tema ha sido actualizado satisfactoriamente.", "url": "/dashboard/subject/index"})
            except Subject.DoesNotExist:
                return render(request, "error.html", {"response": "El tema no existe."})
    else:
        return render(request, "error.html", {"response": "El formulario tenía un error y no pudo ser procesado. Por favor, volvé a intentarlo.", "url": "/dashboard/subject/form"})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def subject_update_state(request, id):
    try:
        obj = Subject.objects.get(id=id)
        obj.is_active = not obj.is_active
        obj.save()
        return redirect("dashboard:subject_index")
    except Subject.DoesNotExist:
        return render(request, "error.html", {"response": "El tema no existe.", "url": "/dashboard/subject/index"})
    except ValueError:
        return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero.", "url": "/dashboard/subject/index"})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def subject_delete(request, id):
    try:
        obj = Subject.objects.get(id=id)
        return render(request, "subject/delete.html", {"subject": obj})
    except Subject.DoesNotExist:
        return render(request, "error.html", {"response": "El tema no existe.", "url": "/dashboard/subject/index"})
    except ValueError:
        return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero.", "url": "/dashboard/subject/index"})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def subject_delete_confirm(request, id):
    try:
        obj = Subject.objects.get(id=id)
        obj.delete()
        return render(request, "success.html", {"response": "El tema ha sido eliminado satisfactoriamente.", "url": "subject/index"})
    except Subject.DoesNotExist:
        return render(request, "error.html", {"response": "El tema no existe.", "url": "subject/index"})
    except IntegrityError:
        return render(request, "error.html", {"response": "El tema está asociado a uno o más posts, por lo que no puede ser eliminado. Podés deshabilitarlo para ocultar los posts asociados al mismo.", "url": "/dashboard/subject/index"})
    except ValueError:
        return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero."})

# logged in - user views - revisado

@login_required
def user_index(request):
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''
    return render(request, "user/index.html", {"usuario": request.user, "avatar": avatar})


@login_required
def user_form(request):
    usuario = request.user
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            data = form.cleaned_data
            usuario.first_name = data["first_name"]
            usuario.last_name = data["last_name"]
            usuario.email = data["email"]
            usuario.password1 = data["password1"]
            usuario.password2 = data["password2"]
            usuario.save()
            return render(request, "success.html", {"response": "El usuario ha sido actualizado satisfactoriamente.", "url": "/dashboard/admin/"})
        else:
            return render(request, "error.html", {"response": "El usuario no se pudo actualizar. Intente nuevamente más tarde."})
    else:
        form = UserEditForm(instance=usuario)
    return render(request, "user/form.html", {"form": form, "usuario": usuario.username, "avatar": avatar})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_edit_avatar(request):

    if request.method == 'POST':
        form_avatar= AvatarForm(request.POST, request.FILES)
        if form_avatar.is_valid():


            try:
                user = User.objects.get(id=form_avatar.cleaned_data['user'].id)
            except User.DoesNotExist:
                return render(request, "error.html", {"response": "El usuario no existe.", "url": "/dashboard/admin"})
            except ValueError:
                return render(request, "error.html", {"response": "El formato del ID enviado no es válido. Debe ser un número entero.", "url": "/dashboard/admin"})

            try:
                old_avatar = Avatar.objects.get(user=user)
                old_avatar.delete()
            except:
                pass

            new_avatar = Avatar(user=user, avatar=form_avatar.cleaned_data['avatar'])
            new_avatar.save()
            request.session['avatar'] = new_avatar.avatar.url
            return render(request, "success.html", {"response": f"El avatar del usuario '{form_avatar.cleaned_data['user'].username}' ha sido actualizado satisfactoriamente.", "url": "/dashboard/user/edit_avatar"})
        else:
            return render(request, "error.html", {"response": "El formulario tenía un error y no pudo ser procesado. Por favor, volvé a intentarlo.", "url": "/dashboard/user/edit_avatar"})
    else:
        form_avatar= AvatarForm()
    return render (request, 'user/edit_avatar.html', {"form":form_avatar})


