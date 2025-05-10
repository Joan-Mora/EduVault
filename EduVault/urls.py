from django.urls import path
from .views import home
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView
from .views import ArchivoViewSet, MateriaViewSet, EtiquetaViewSet
from . import views
from django.conf.urls.static import static
from django.conf import settings
router = DefaultRouter()
router.register(r'archivos', ArchivoViewSet, basename='archivo')
router.register(r'materias', MateriaViewSet)
router.register(r'etiquetas', EtiquetaViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('api/', include(router.urls)),
    path('gauss-jordan/', views.gauss_jordan_view, name='gauss_jordan'),  # Vista para el método de Gauss-Jordan
    path('inicio/', views.home, name='inicio'),  # Vista para la página de inicio
    path('mis_archivos/', views.mis_archivos, name='mis_archivos'),  # Vista para la página de mis archivos
    path('subir_archivo/', views.subir_archivo, name='subir_archivos'),  # Vista para subir archivos
    path('perfil/', views.perfil, name='perfil'),  # Vista para el perfil del usuario
    path('publico/', views.publico_view, name='publico'),  # Vista para archivos públicos
    path('contacto/', views.contacto, name='contacto'),  # Vista para la página de contacto
    path ('logout/', RedirectView.as_view(url=('accounts/logout/'))),
    path('eliminar/<int:archivo_id>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('confirmar_eliminar/<int:archivo_id>/', views.confirmar_eliminar, name='confirmar_eliminar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)