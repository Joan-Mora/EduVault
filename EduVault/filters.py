import django_filters
from django import forms
from .models import Archivo, Materia, Etiqueta
from django.utils import timezone
from datetime import timedelta

class ArchivoFilter(django_filters.FilterSet):
    materia = django_filters.ModelChoiceFilter(
        queryset=Materia.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white'})
    )
    etiquetas = django_filters.ModelMultipleChoiceFilter(
        queryset=Etiqueta.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select bg-dark text-white'})
    )
    tipo = django_filters.ChoiceFilter(
        choices=[
            ('pdf', 'PDF'),
            ('word', 'Word'),
            ('excel', 'Excel'),
            ('imagen', 'Imagen(JPG, PNG)'),
            ('video', 'Video(MP4, MKV)'),
            ('otro', 'Otro'),
        ],
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white'})
    )
    
    titulo = django_filters.CharFilter(lookup_expr='icontains', label='Título')

    # Filtro de fecha
    fecha = django_filters.ChoiceFilter(
        choices=[
            ('mas_reciente', 'Más reciente'),
            ('mas_antiguo', 'Más antiguo'),
            ('hace_7_dias', 'Hace 7 días'),
            ('hace_30_dias', 'Hace 30 días'),
        ],
        method='filter_by_fecha',
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white'})
    )

    def filter_by_fecha(self, queryset, name, value):
        if value == 'mas_reciente':
            return queryset.order_by('-fecha_subida')
        elif value == 'mas_antiguo':
            return queryset.order_by('fecha_subida')
        elif value == 'hace_7_dias':
            fecha_limite = timezone.now() - timedelta(days=7)
            return queryset.filter(fecha_subida__gte=fecha_limite)
        elif value == 'hace_30_dias':
            fecha_limite = timezone.now() - timedelta(days=30)
            return queryset.filter(fecha_subida__gte=fecha_limite)
        return queryset

    class Meta:
        model = Archivo
        fields = ['materia', 'etiquetas', 'tipo', 'titulo', 'fecha']
