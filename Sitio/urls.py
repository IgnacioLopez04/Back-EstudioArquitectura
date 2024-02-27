from django.urls import path, include, re_path
from rest_framework import routers
from . import views


#versiones de api
router = routers.DefaultRouter()
#Va a generar las acciones de get, post, put, delete por defecto, asi que no se hace de manera manual
router.register(r'arquitectos', views.ArquitectoView, 'arquitectos')
router.register(r'estudio', views.EstudioView, 'estudio')
router.register(r'clientes', views.ClienteView, 'clientes')
router.register(r'proyectos', views.ProyectoView, 'proyectos')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/proyectos/cliente/<str:tk_client>/', views.ProyectoClienteView.as_view(), name='proyectos-cliente'),
    path('api/proyectos/images/<str:tk_project>', views.obtener_imagenes_proyecto, name='images'),
    path('api/proyectos/images/<str:img>/<str:tk_project>', views.borrar_imagen, name='borrar-img'),
    path('api/imagenesGallery', views.buscar_imagenes, name='buscar-imagenes-galeria'),
    path('api/destacados/', views.proyectos_destacados, name='proyectos-destacados'),
    path('api/proyectos/publicos', views.proyectos_publicos, name='proyectos-publicos'),
    # re_path('login', views.login, name='login'),
    # re_path('test', views.test, name='test'),
    
]
