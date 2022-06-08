from django.contrib import admin

from business_layer.models import *

# Register your models here.

admin.site.register(Subject)
admin.site.register(Post)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Avatar)