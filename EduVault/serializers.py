from rest_framework import serializers
from .models import Archivo, Materia, Etiqueta
from django.contrib.auth.models import User

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['id', 'nombre']  # Solo devolver 'id' y 'nombre'

class ArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = '__all__'

class ArchivoCreateSerializer(serializers.ModelSerializer):
    materia = serializers.PrimaryKeyRelatedField(queryset=Materia.objects.all())  # Aquí cambiamos a PrimaryKeyRelatedField

    class Meta:
        model = Archivo
        fields = '__all__'
