from django.db import models
from django.contrib.auth.models import User


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
    archivo = models.FileField(upload_to='archivos/', null=False)
    def __str__(self):
        return self.titulo

    
class ArchivoFile(models.Model):
    archivo = models.FileField(upload_to='archivos/')
    archivo_relacionado = models.ForeignKey(Archivo, related_name='archivos', on_delete=models.CASCADE)

    def __str__(self):
        return self.archivo.name