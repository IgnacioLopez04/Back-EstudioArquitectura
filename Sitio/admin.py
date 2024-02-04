from django.contrib import admin
from .models import Proyecto, Cliente, Arquitecto, Estudio, ImagenesProyecto
# Register your models here.

class ImagenesProyectoAdmin(admin.TabularInline):
    model = ImagenesProyecto

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion', 'ciudad', 'descripcion']
    inlines = [
        ImagenesProyectoAdmin
    ]

admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Cliente)
admin.site.register(Arquitecto)
admin.site.register(Estudio)