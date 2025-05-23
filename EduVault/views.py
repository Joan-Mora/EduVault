from django.shortcuts import render,redirect,get_object_or_404
import os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArchivoForm
from .filters import ArchivoFilter
from rest_framework import viewsets, permissions, status
from .models import Archivo, Materia, Etiqueta, ArchivoFile
from .serializers import ArchivoSerializer, MateriaSerializer, EtiquetaSerializer
from rest_framework.response import Response
from django.db import transaction
import numpy as np
from fractions import Fraction
from .models import Profile
from django.utils import timezone
from datetime import timedelta
from django.http import FileResponse

def descargar_archivo(request, archivo_id):
    archivo = get_object_or_404(Archivo, pk=archivo_id)
    response = FileResponse(archivo.archivo.open(), as_attachment=True, filename=archivo.archivo.name.split('/')[-1])
    return response

@login_required
def perfil(request):
    profile = Profile.objects.get_or_create(autor=request.user)[0]  # ✅ asegura que exista

    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        if avatar:
            # ✅ Eliminar avatar anterior si existe
            if profile.avatar:
                profile.avatar.delete(save=False)

            # ✅ Asignar nuevo avatar
            profile.avatar = avatar
            profile.save()

            return redirect('perfil')  # redirige a la misma vista

    return render(request, 'perfil.html', {'profile': profile})


@login_required
def vista_con_sidebar(request):
    profile = Profile.objects.get_or_create(autor=request.user)[0]
    return render(request, 'base.html', {'profile': profile})


def contacto(request):
    return render(request, 'contacto.html')



def generar_matriz(tamano):
    A = np.random.randint(1, 10, size=(tamano, tamano))
    b = np.random.randint(1, 10, size=(tamano, 1))
    matriz_aumentada = np.hstack((A, b))
    return matriz_aumentada


def gauss_jordan(matriz_aumentada):
    # Convertir a float para evitar errores de precisión
    matriz = [[float(valor) for valor in fila] for fila in matriz_aumentada]
    n = len(matriz)
    m = len(matriz[0])
    pasos = []

    for i in range(n):
        # Verificar que el pivote no sea cero (o cercano a cero)
        if abs(matriz[i][i]) < 1e-9:
            for j in range(i + 1, n):
                if abs(matriz[j][i]) > 1e-9:
                    matriz[i], matriz[j] = matriz[j], matriz[i]
                    pasos.append(f"Intercambiando fila {i+1} con fila {j+1}")
                    break
            else:
                pasos.append(f"No se pudo encontrar un pivote válido en la columna {i+1}. Sistema sin solución o infinitas soluciones.")
                return matriz, [], pasos

        # Normalizar la fila para que el pivote sea 1
        pivote = matriz[i][i]
        for j in range(m):
            matriz[i][j] /= pivote
        pasos.append(f"Dividiendo la fila {i+1} por {pivote} para hacer el pivote igual a 1")

        # Hacer ceros en las demás filas
        for j in range(n):
            if j != i:
                factor = matriz[j][i]
                for k in range(m):
                    matriz[j][k] -= factor * matriz[i][k]
                pasos.append(f"Haciendo ceros en la columna {i+1} para la fila {j+1}")

    # Obtener la solución redondeada a 4 decimales
    solucion = [round(fila[-1], 4) for fila in matriz]

    # Redondear la matriz final también
    matriz_redondeada = [[round(valor, 4) for valor in fila] for fila in matriz]

    return matriz_redondeada, solucion, pasos


def gauss_jordan_view(request):
    if request.method == 'POST':
        tamano_str = request.POST.get('tamano', '').strip()

        # Validar el tamaño de la matriz
        if not tamano_str.isdigit() or int(tamano_str) < 1:
            error_message = "Por favor, ingresa un número válido y positivo para el tamaño de la matriz."
            return render(request, 'pagina_gauss.html', {
                'error_message': error_message,
                'tamano': 2
            })

        tamano = int(tamano_str)

        # MATRIZ ALEATORIA
        if 'generar_matriz_aleatoria' in request.POST:
            matriz = np.random.randint(1, 10, size=(tamano, tamano))
            b = np.random.randint(1, 10, size=(tamano, 1))
            matriz_aumentada = np.hstack((matriz, b)).astype(float)

            try:
                matriz_final, solucion, pasos = gauss_jordan(matriz_aumentada.tolist())
            except Exception as e:
                return render(request, 'pagina_gauss.html', {
                    'tamano': tamano,
                    'matriz': matriz_aumentada.tolist(),
                    'error_message': f"Ocurrió un error resolviendo la matriz: {str(e)}",
                    'rango_tamano': range(tamano),
                })

            context = {
                'tamano': tamano,
                'matriz': np.round(matriz_aumentada, 4).tolist(),
                'solucion': solucion,
                'pasos': pasos,
                'matriz_final': matriz_final,
                'rango_tamano': range(tamano),
            }
            return render(request, 'pagina_gauss.html', context)

        # INGRESAR MANUALMENTE
        elif 'ingresar_matriz_manualmente' in request.POST:
            return render(request, 'pagina_gauss.html', {
                'tamano': tamano,
                'rango_tamano': range(tamano),
                'rango_tamano_plus': range(tamano + 1),
                'ingresando': True
            })

        # PROCESAR MATRIZ MANUAL
        else:
            matriz_aumentada = []
            for i in range(tamano):
                fila = []
                for j in range(tamano + 1):
                    val = request.POST.get(f'valor_{i}_{j}', '').strip()
                    try:
                        valor = float(val) if val != '' else 0.0
                    except ValueError:
                        error_message = f"Valor inválido en posición [{i+1},{j+1}]."
                        return render(request, 'pagina_gauss.html', {
                            'error_message': error_message,
                            'tamano': tamano,
                            'rango_tamano': range(tamano),
                            'rango_tamano_plus': range(tamano + 1),
                            'ingresando': True
                        })
                    fila.append(valor)
                matriz_aumentada.append(fila)

            try:
                matriz_final, solucion, pasos = gauss_jordan(matriz_aumentada)
            except Exception as e:
                return render(request, 'pagina_gauss.html', {
                    'tamano': tamano,
                    'matriz': matriz_aumentada,
                    'error_message': f"Ocurrió un error resolviendo la matriz: {str(e)}",
                    'rango_tamano': range(tamano),
                })

            context = {
                'tamano': tamano,
                'matriz': np.round(matriz_aumentada, 4).tolist(),
                'solucion': solucion,
                'pasos': pasos,
                'matriz_final': matriz_final,
                'rango_tamano': range(tamano),
            }
            return render(request, 'pagina_gauss.html', context)

    # GET request por defecto
    return render(request, 'pagina_gauss.html', {'tamano': 2})



# Vista que maneja la solicitud para generar y resolver la matriz
def resolver_matriz(request, tamano):
    # Generamos la matriz aumentada de tamaño 'tamano'
    matriz_aumentada = generar_matriz(tamano)
    
    # Aplicamos el método de Gauss-Jordan y obtenemos los pasos
    resultado, pasos = gauss_jordan(matriz_aumentada)
    
    # Pasamos la matriz, la solución y los pasos al template
    return render(request, 'pagina_gauss.html', {'matriz': matriz_aumentada.tolist(), 'solucion': resultado.tolist(), 'pasos': pasos})



@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def subir_archivo(request):
    materias = Materia.objects.all()
    etiquetas = Etiqueta.objects.all()

    form = ArchivoForm(request.POST or None, request.FILES or None)  # Asegurarse de que 'form' siempre esté definido

    if request.method == 'POST':
        if form.is_valid():
            try:
                with transaction.atomic():
                    archivo = form.save(commit=False)
                    print(f"Archivo subido: {archivo.archivo}")
                    archivo.autor = request.user
                    archivo.save()
                    form.save_m2m()

                    messages.success(request, 'Archivo subido correctamente.')
                    return redirect('mis_archivos')

            except Exception as e:
                print(f"Error al guardar el archivo: {e}")
                messages.error(request, 'Hubo un error al guardar el archivo. Intenta de nuevo.')

        else:
            print(form.errors)  # Imprimir los errores de validación
            messages.error(request, 'Formulario no válido. Revisa los errores.')

    return render(request, 'subir_archivo.html', {
        'form': form,
        'materias': materias,
        'etiquetas': etiquetas
    })

@login_required
def mis_archivos(request):
    # 1) Archivos exclusivos del usuario, para el contador
    archivos_usuario = Archivo.objects.filter(autor=request.user).order_by('-fecha_subida')
    
    # 2) Archivos a mostrar: privados de este usuario + públicos de otros
    privados = archivos_usuario
    publicos = Archivo.objects.filter(publico=True).exclude(autor=request.user)
    archivos_mostrar = (privados | publicos).order_by('-fecha_subida')
    
    # 3) Aplica filtros (título, tipo, etiqueta…) sobre el conjunto a mostrar
    archivo_filter = ArchivoFilter(request.GET, queryset=archivos_mostrar)
    archivos_filtrados = archivo_filter.qs
    
    # 4) Colores para extensiones (si lo usas en el template)
    colores = {
        ".pdf": "#dc3545",   # rojo
        ".jpg": "#0d6efd",   # azul
        ".png": "#0d6efd",   # azul
        ".mp4": "#198754",   # verde
        ".docx": "#6610f2",  # morado
        ".xlsx": "#20c997",  # verde esmeralda
        "default": "#6c757d" # gris
    }

    return render(request, 'mis_archivos.html', {
        'archivos_usuario': archivos_usuario,      # para el contador
        'archivos': archivos_filtrados,            # para el grid
        'filter': archivo_filter,
        'colores': colores,
    })


@login_required
def publico_view(request):
    etiquetas = Etiqueta.objects.all()
    archivos = Archivo.objects.filter(publico=True)

    # Filtrar por fecha
    fecha_filtro = request.GET.get('fecha')
    if fecha_filtro:
        if fecha_filtro == 'mas_reciente':
            archivos = archivos.order_by('-fecha_subida')
        elif fecha_filtro == 'mas_antiguo':
            archivos = archivos.order_by('fecha_subida')
        elif fecha_filtro == 'hace_7_dias':
            fecha_limite = timezone.now() - timedelta(days=7)
            archivos = archivos.filter(fecha_subida__gte=fecha_limite)
        elif fecha_filtro == 'hace_30_dias':
            fecha_limite = timezone.now() - timedelta(days=30)
            archivos = archivos.filter(fecha_subida__gte=fecha_limite)

    # Filtrado por otros parámetros
    if request.GET.get('etiqueta'):
        archivos = archivos.filter(etiquetas__id=request.GET['etiqueta'])

    filter = ArchivoFilter(request.GET, queryset=archivos)

    return render(request, 'publico.html', {
        'archivos': filter.qs,
        'filter': filter,
        'etiquetas': etiquetas,
    })

@login_required
def confirmar_eliminar(request, archivo_id):
    archivo = get_object_or_404(Archivo, id=archivo_id)
    
    if request.method == 'POST':
        archivo.delete()
        return redirect('mis_archivos')  # Redirigir a la lista de archivos o a donde prefieras

    return render(request, 'confirmar_eliminar.html', {'archivo': archivo})

@login_required
def eliminar_archivo(request, archivo_id):
    archivo = get_object_or_404(Archivo, id=archivo_id, autor=request.user)

    if request.method == 'POST':
        # Eliminar archivo del almacenamiento (S3)
        if archivo.archivo:
            archivo.archivo.delete(save=False)

        # Eliminar el registro de la base de datos
        archivo.delete()

        messages.success(request, 'Archivo eliminado correctamente.')
        return redirect('mis_archivos')

    messages.error(request, 'Acción no permitida.')
    return redirect('mis_archivos')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado: solo el dueño puede editar/borrar su archivo.
    Los archivos públicos solo pueden ser borrados por superusuarios.
    """

    def has_object_permission(self, request, view, obj):
        # Todos pueden ver (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Si el archivo es público, solo superuser puede borrarlo
        if obj.publico and request.method == 'DELETE':
            return request.user.is_superuser

        # Solo el autor puede editar/borrar su archivo
        return obj.autor == request.user

class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return ArchivoSerializer
        return ArchivoSerializer
    
    def get_queryset(self):
        
        if self.request.user.is_superuser:
            # Si es superusuario, puede ver todos los archivos, incluso los públicos
            return Archivo.objects.all()
        else:
            # De lo contrario, solo mostrar los archivos del usuario
            return Archivo.objects.filter(autor=self.request.user)

    def perform_create(self, serializer):
        # Asocia el archivo al usuario que lo sube
        serializer.save(autor=self.request.user)

    def perform_destroy(self, instance):
        # Solo permite borrar archivos públicos si el usuario es superuser
        if instance.publico and not self.request.user.is_superuser:
            raise permissions.PermissionDenied("No tienes permiso para borrar este archivo.")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ArchivosPublicosViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Archivo.objects.filter(publico=True)
    serializer_class = ArchivoSerializer