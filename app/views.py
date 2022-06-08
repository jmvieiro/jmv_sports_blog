from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from app.forms import *
from business_layer.models import *
from business_layer.views import *


class Index(ListView):
    model = Post
    template_name = "index.html"

    def get(self, request):
        key_word = request.GET.get('key_word', None)
        context = {}
        context['key_word'] = key_word
        context['posts'] = get_posts(is_active=True, key_word=key_word)
        context['authors'] = get_authors()
        context['subjects'] = get_subjects()
        if (self.request.user.is_authenticated):
            context['mensajesNoLeidos'] = len(Message.objects.filter(
                receiver=self.request.user, is_read=False))
        return render(request, self.template_name, context)


# Utilizo ListView (en lugar de DetailView) para poder usar el template de lista y mostrar un mensaje cuando no se encuentra el post. Con DetailView genera error 404 Page Not Found.
class PostDetail(ListView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['authors'] = get_authors()
        context['subjects'] = get_subjects()
        context['post'] = get_post_by_id(self.kwargs['pk'])
        if context['post'] is None:
            context['response'] = "¡Ups! El post no existe."
        else:
            context['comments'] = get_post_comments(context["post"])
            context['form'] = CommentForm()
        return context


def post_like(request, id):
    try:
        obj = Post.objects.get(id=id)
        obj.likes += 1
        obj.save()
        return redirect("blogjmv:post_detail", id)
    except Post.DoesNotExist: 
        return render(request, "post_detail.html", {"response": "El post no existe o no tenés permisos para comentarlo."})
    except ValueError:
        return render(request, "post_detail.html", {"response": "El post no existe o no tenés permisos para comentarlo."})
        

class PostBySubject(ListView):
    model = Post
    template_name = "post_by_subject.html"

    def get_context_data(self, **kwargs):
        context = super(PostBySubject, self).get_context_data(**kwargs)
        context['authors'] = get_authors()
        context['subjects'] = get_subjects()
        context['subject'] = get_subject_by_id(self.kwargs['pk'])
        if context['subject'] is None:
            context['response'] = "¡Ups! El tema no existe."
        else:
            context['posts'] = get_posts_by_subject(self.kwargs['pk'])
        return context


class PostByAuthor(ListView):
    model = Post
    template_name = "post_by_author.html"

    def get_context_data(self, **kwargs):
        context = super(PostByAuthor, self).get_context_data(**kwargs)
        context['authors'] = get_authors()
        context['subjects'] = get_subjects()
        context['author'] = get_author_by_id(self.kwargs['pk'])
        if context['author'] is None:
            context['response'] = "¡Ups! El autor no existe."
        else:
            context['posts'] = get_posts_by_author(self.kwargs['pk'])
        return context


class About(ListView):
    queryset = []
    template_name = "about.html"

# revisado


def login_request(request):
    if request.method == "POST":
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    request.session['avatar'] = Avatar.objects.get(user=user).avatar.url
                except:
                    request.session['avatar'] = '/static/dist/img/user-placeholder.png'
                return redirect("blogjmv:index")
            else:
                return render(request, "login.html", {"form": form, "response": "El usuario o la contraseña son incorrectos."})
        else:
            return render(request, "login.html", {"form": form, "response": "El usuario o la contraseña son incorrectos."})
    return render(request, "login.html", {"form": UserLoginForm()})

# revisado


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("blogjmv:index")
        else:
            if 'username' in form.errors:
                return render(request, "register.html", {"form": form, "response": "El usuario ya existe."})
            if "password2" in form.errors:
                return render(request, "register.html", {"form": form, "response": "Las contraseñas no coinciden."})
            return render(request, "register.html", {"form": form, "response": "No se pudo crear el usuario."})
    return render(request, "register.html", {"form": UserRegistrationForm()})


# logged in - comment views


@login_required
def comment_create(request, id):
    form = CommentForm(request.POST)
    if form.is_valid():
        try:
            data = form.cleaned_data
            post = Post.objects.get(id=id)
            obj = Comment(text=data.get("text"),
                          author=request.user, post=post)
            obj.save()
            return redirect("blogjmv:post_detail", id)
        except Post.DoesNotExist:
            return redirect("blogjmv:post_detail", id)

    else:
        return redirect("blogjmv:post_detail", id)
