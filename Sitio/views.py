from rest_framework.exceptions import NotFound
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .serializer import ArquitectoSerealizer, ClienteSerealizer, ProyectoSerealizer, EstudioSerealizer, UserSerializer
from .models import Arquitecto, Cliente, Estudio, Proyecto, ImagenesProyecto
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import ImagenesProyecto, Proyecto
from random import sample
from .token import ProjectTokenGenerator, ClientTokenGenerator
from rest_framework import status
import cloudinary
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



#Va a realizar todo el CRUD del arquitecto
class ArquitectoView(viewsets.ModelViewSet):
    serializer_class = ArquitectoSerealizer
    queryset = Arquitecto.objects.all()
    
#Va a realizar todo el CRUD del cliente
class ClienteView(viewsets.ModelViewSet):
    serializer_class = ClienteSerealizer
    queryset = Cliente.objects.all()
    
    def perform_create(self, serializer):
        cliente = serializer.save()
        
         # Token
        token_generator = ClientTokenGenerator()
        token = token_generator.make_token(cliente)
        
        cliente.token = token
        cliente.save()
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_field = 'token'  # Utiliza el campo por el cual quieres buscar

        # Obtener el valor del campo de búsqueda desde la URL
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)

        if lookup_value is None:
            raise NotFound("No se proporcionó el valor del campo de búsqueda.")

        # Filtrar el queryset por el campo de búsqueda
        filter_kwargs = {lookup_field: lookup_value}
        obj = queryset.filter(**filter_kwargs).first()

        if obj is None:
            raise NotFound("No se encontró el objeto con el valor proporcionado.")

        self.check_object_permissions(self.request, obj)
        return obj
    
#Va a realizar todo el CRUD del Proyecto
class ProyectoView(viewsets.ModelViewSet):
    serializer_class = ProyectoSerealizer
    queryset = Proyecto.objects.all()
    
    def perform_create(self, serializer):
        proyecto = serializer.save()
        
        #Token
        token_generator = ProjectTokenGenerator()
        token = token_generator.make_token(proyecto)
        
        proyecto.token = token
        proyecto.save()
        
        #Manejo de imagenes
        imagenes = self.request.FILES.getlist('imagenes[]')

        for imagen in imagenes:
            ImagenesProyecto.objects.create(proyecto=proyecto, imagen=imagen)
            
    def perform_destroy(self, instance):
        # Eliminar las imágenes asociadas al proyecto
        imagenes_proyecto = ImagenesProyecto.objects.filter(proyecto=instance)
        for img in imagenes_proyecto:
            print(type(img))
            cloudinary.uploader.destroy(img.imagen.public_id)
            img.delete()

        # Finalmente, eliminar el proyecto
        instance.delete()
        
    def perform_update(self, serializer):
        proyecto = serializer.save()
        
        imagenes = self.request.FILES.getlist('imagenes[]')
        for imagen in imagenes:
            ImagenesProyecto.objects.create(proyecto=proyecto, imagen=imagen)
        
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_field = 'token'  # Utiliza el campo por el cual quieres buscar

        # Obtener el valor del campo de búsqueda desde la URL
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs.get(lookup_url_kwarg)

        if lookup_value is None:
            raise NotFound("No se proporcionó el valor del campo de búsqueda.")

        # Filtrar el queryset por el campo de búsqueda
        filter_kwargs = {lookup_field: lookup_value}
        obj = queryset.filter(**filter_kwargs).first()

        if obj is None:
            raise NotFound("No se encontró el objeto con el valor proporcionado.")

        self.check_object_permissions(self.request, obj)
        return obj
    
# Busca los proyectos de un cliente
class ProyectoClienteView(generics.ListAPIView):
    serializer_class = ProyectoSerealizer
    
    def get_queryset(self):
        cliente_tk = self.kwargs['tk_client']
        client = Cliente.objects.filter(token=cliente_tk).first()
        
        return Proyecto.objects.filter(cliente=client.pk)
    
#Va a realizar todo el CRUD del Estudio
class EstudioView(viewsets.ModelViewSet):
    serializer_class = EstudioSerealizer
    queryset = Estudio.objects.all()
    
    def create(self, request, *args, **kwargs):
        # Verificar si ya existe un estudio en la base de datos
        existing_studio = Estudio.objects.first()
        if existing_studio:
            # Si ya existe, actualiza los datos del estudio existente en lugar de crear uno nuevo
            serializer = self.get_serializer(existing_studio, data=request.data)
        else:
            # Si no existe, crea un nuevo objeto de estudio
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # Obtener el objeto de estudio existente
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
 
def obtener_imagenes_proyecto(request,tk_project):
    proyecto = get_object_or_404(Proyecto, token=tk_project)
    imagenes = ImagenesProyecto.objects.filter(proyecto=proyecto)
    
    data = {
        'proyecto_nombre': proyecto.nombre,
        'imagenes': [imagen.imagen.url for imagen in imagenes],
    }

    return JsonResponse(data)

# @csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def borrar_imagen(request, img, tk_project):
    proyecto = get_object_or_404(Proyecto, token=tk_project)
    imagen = ImagenesProyecto.objects.filter(proyecto=proyecto)
    
    for item in imagen:
        if str(item.imagen) == img:
            imagen = item
    
    cloudinary.uploader.destroy(imagen.imagen.public_id)
    imagen.delete()
    return JsonResponse({'detail':'Imagen eliminada'}, status=status.HTTP_200_OK)

def buscar_imagenes(resquest):
    images = ImagenesProyecto.objects.all()
    if not images:
        data = {}
        return JsonResponse(data)
    random_images = sample(list(images), 5)
    
    data = {
        'imagenes': [imagen.imagen.url for imagen in random_images],
    }
    
    return JsonResponse(data)

def proyectos_destacados(request):
    proyectos = Proyecto.objects.filter(destacado=True)
    if not proyectos:
        data = {}
        return JsonResponse(data)
    random_proyectos = sample(list(proyectos), 3)
    imagenes = {}
    
    for project in random_proyectos:
        first_image = ImagenesProyecto.objects.filter(proyecto=project).first()
        
        if first_image:
            imagenes[project.id] = {
                'proyecto': first_image.proyecto.id,
                'imagen': first_image.imagen.url,
            }
        
    serialized_project = {
        'proyectos': [{'nombre':project.nombre, 'descripcion': project.descripcion, 'id': project.id, 'token': project.token} for project in random_proyectos],
        'imagenes':imagenes,
    }
    
    return JsonResponse(serialized_project, safe=False)

def proyectos_publicos(request):
    proyectos = Proyecto.objects.filter(esPrivado=False)
    imagenesTodas = ImagenesProyecto.objects.all()
    
    serialized_project = {
        'proyectos': [],
    }
    
    for project in proyectos:
        imagenes_proyecto = imagenesTodas.filter(proyecto=project)
    
        serialized_project['proyectos'].append({
            'token': project.token,
            'id': project.id,
            'nombre':project.nombre, 
            'descripcion': project.descripcion,
            'ciudad':project.ciudad,
            'metrosTotales':project.metrosTotales,
            'metrosCubiertos':project.metrosCubiertos,
            'habitaciones':project.habitaciones,
            'baños': project.baños,
            'imagenes': [{'url': imagen.imagen.url} for imagen in imagenes_proyecto],
        })
    
    return JsonResponse(serialized_project, safe=False)

# Extiende la forma en la que serializamos el token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer