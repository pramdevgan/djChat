from django.contrib import admin

from .models import Channels, Category, Server

# Register your models here.

admin.site.register(Category)
admin.site.register(Channels)
admin.site.register(Server)
