# Blog proyecto académico sobre Python & Django

Blog "JMV Sports" con Python & Django.

## Comenzando con Python & Django

Este proyecto fue inicializado con Python [https://www.python.org/] y Django [https://www.djangoproject.com/].

## Sobre el proyecto

Este proyecto fue llevado a cabo con fines académicos, tratando de respetar las mejores prácticas obtenidas en clase, en el marco del curso de Python brindado por CoderHouse.

El proyecto consiste en la realización de un blog, denominado JMV Sports, a través de la cual se podrán probar las principales funcionalidades aprendidas.

Para la realización del proyecto, se instalaron las siguientes dependencias:

- Estilos basados en bootstrap, tomando como base el template AdminLTE. https://adminlte.io/themes/v3/index.html.
- "Django Crispy Forms" para implementar estilos basados en Bootstrap a los formularios Django [https://django-crispy-forms.readthedocs.io/en/latest/index.html]
- "Django Pillow" para el manejo de imágenes en Python.
    
## Instalación

- Instalar Python desde el sitio oficial.
- Clonar el repositorio: *git clone https://github.com/jmvieiro/jmv_sports_blog*
- Instalar las dependencias: django y pillow
- Crear superusuario -optativo-.
- Iniciar la aplicación: *py manage.py runserver*

### Modelo: business_layer

- Subject: temas incluidos en el blog, referidos al mundo del deporte. Por ejemplo, Fúbol, Básquet, Tenis, etc.
- Post: cada entrada del blog, que contiene la información a ser compartida mediante los usuarios en la aplicación. 
- Comment: comentario que dejan los usuarios registrados en los posts.
- Message: mensaje que se envía entre los distintos usuarios del sistema, a través de un chat disponible en la aplicación.
- Avatar: imagen que corresponde e identifica en el sistema a cada usuario registrado.

### App, aplicación del blog propiamente dicha

Aplicación donde se interactúa con el blog en sí mismo, donde los visitantes pueden visualizar los post publicados.
Permite la búsqueda por palabras claves, por autor y por tema: post_by_author y post_by_subject.
Permite la visualización del detalle del post, "post_detail".
Permite la registración de nuevos usuarios, "register".
Permite el acceso como usuario registrado, "login".
Permite a los usuarios logueados, comentar los distintos posts.
Contiene una página "about" con información del creador del blog.

### Dashboard, administración del contenido del blog

Aplicación que permite a los usuarios registrados administrar el contenido del blog.

Principales funcionalidades:

#### Subjects (temas):
- Solo pueden ser creados, editados o elminados por el usuario administrador (superuser). Se puede pausar la visualización de un tema y sus posts asociados "ocultándolo" (inactivo).
#### Posts:
- Publicación de un post por parte del usuario -autor-.
- Edicición de un post por parte de un usuario, si este fue el autor del mismo. El usuario administrador puede modificar cualquier post de cualquier autor.
#### Avatar:
- Incorporar un Avatar a los usuarios registrados.
- Solo el usuario administrador puede incorporar o editar avatars a los distitntos usuarios. El resto de los usuarios solo pueden visualizarlo.
#### Chat:
- Aplicación de mensajería entre los distintos usuarios del sistema.
#### Perfil de usuario:
- Cada usuario puede modificar su perfil (nombre, apellido, email y contraseña). Al usuario no administrador no se le permite editar su avatar, quedando disponible únicmaente para el usuario administrador.

### Congiuración del sistema:

A efectos de facilitar la creación de usuarios, están comentadas las validaciones de seguridad de la contraseña en el archivo "settings.py" dentro del proyecto.
### Casos de prueba

Se listan diversos casos de prueba en el archivo "JMV Sports - Blog - casos de prueba.pdf".

### Video

https://drive.google.com/drive/folders/1m8zZpA66z3u7Gey3XWHaj1z5Mh_U3So_?usp=sharing