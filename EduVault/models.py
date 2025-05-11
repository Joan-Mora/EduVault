from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now
import os

class Profile(models.Model):
    autor = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.autor.username
    
class Materia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
   

    def __str__(self):
        return self.nombre	

class Etiqueta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Archivo(models.Model):
    TIPO_CHOICES = [
        ('pdf', 'PDF'),
        ('word', 'Word'),
        ('excel', 'Excel'),
        ('imagen', 'Imagen(JPG, PNG)'),
        ('video', 'Video(MP4, MKV)'),
        ('otro', 'Otro'),
    ]
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    publico = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='archivos/temp/', null=False)

    def save(self, *args, **kwargs):
        is_new = self._state.adding and self.archivo
        super().save(*args, **kwargs)

        if is_new:
            original_path = self.archivo.path
            ext = os.path.splitext(original_path)[1]
            filename = f"{self.pk}_{now().strftime('%Y%m%d%H%M%S')}{ext}"

            new_folder = 'archivos_publicos' if self.publico else 'archivos'
            new_path_rel = os.path.join(new_folder, filename)
            new_path_abs = os.path.join(settings.MEDIA_ROOT, new_path_rel)

            # Crear carpeta si no existe
            os.makedirs(os.path.dirname(new_path_abs), exist_ok=True)

            # Mover el archivo
            os.rename(original_path, new_path_abs)

            # Actualizar la ruta en el modelo
            self.archivo.name = new_path_rel
            super().save(update_fields=['archivo'])

    def __str__(self):
        return self.titulo
    
class ArchivoFile(models.Model):
    archivo = models.FileField(upload_to='archivos/')
    archivo_relacionado = models.ForeignKey(Archivo, related_name='archivos', on_delete=models.CASCADE)

    def __str__(self):
        return self.archivo.name