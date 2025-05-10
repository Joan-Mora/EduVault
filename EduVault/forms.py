from django import forms
from .models import Archivo
import os


class MatrizForm(forms.ModelForm):
     tamano= forms.IntegerField(min_value=2, label='Tamaño de la matriz')


class ArchivoForm(forms.ModelForm):
    archivos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': False}), 
        required=False
    )

    class Meta:
        model = Archivo
        fields = ['titulo', 'descripcion', 'archivo', 'materia', 'etiquetas', 'tipo', 'publico']

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')

        max_size = 100 * 1024 * 1024  # 100MB
        if archivo.size > max_size:
            raise forms.ValidationError(f"El archivo '{archivo.name}' es demasiado grande. El tamaño máximo permitido es 100MB.")
        
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.docx', '.xlsx', '.mp4', '.mkv', '.avi']
        _, ext = os.path.splitext(archivo.name.lower())
        
        if ext not in allowed_extensions:
            raise forms.ValidationError(f"La extensión '{ext}' no está permitida. Solo se permiten los siguientes formatos: {', '.join(allowed_extensions)}.")
        
        return archivo
