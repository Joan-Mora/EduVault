from django.contrib import admin
from .models import Materia, Etiqueta, Archivo, Profile, ArchivoFile


class ArchivoAdmin(admin.ModelAdmin):
     
     list_display = ('titulo','materia','autor','fecha_subida','tipo')
     search_fields = ('titulo', 'materia__nombre', 'autor__username')
     list_filter = ('materia', 'tipo', 'fecha_subida')


class MateriaAdmin(admin.ModelAdmin):
     
     list_display = ('nombre',)

class EtiquetaAdmin(admin.ModelAdmin):
         
     list_display = ('nombre',)

admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Etiqueta, EtiquetaAdmin)
admin.site.register(Profile)
