from rest_framework import serializers
from .models import Arquitecto, Cliente, Estudio, Proyecto, ImagenesProyecto


#Vamos a convertir los tipos de datos de Python a Json
class ArquitectoSerealizer(serializers.ModelSerializer):
    class Meta:
        model = Arquitecto
        fields = '__all__'
        
class ClienteSerealizer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class EstudioSerealizer(serializers.ModelSerializer):
    class Meta:
        model = Estudio
        fields = '__all__'
        
class ProyectoSerealizer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'
        
class ImagenesProyectoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImagenesProyecto
        fields = ('imagen', 'proyecto')