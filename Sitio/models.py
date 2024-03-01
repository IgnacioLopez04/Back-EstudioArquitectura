from django.db import models
from django.core.validators import FileExtensionValidator
from cloudinary.models import CloudinaryField


# Create your models here.
class Arquitecto(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    telefono = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.nombre
    
class Estudio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    correo = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    token = models.CharField(max_length=200, null=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    dni = models.IntegerField(null=False)
    
    def __str__(self):
        return self.nombre
    
class Proyecto(models.Model):
    token = models.CharField(max_length=200, null=True)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    esPrivado = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)
    metrosTotales = models.IntegerField(null=True)
    metrosCubiertos = models.IntegerField(null=True)
    habitaciones = models.IntegerField(null=True)
    baños = models.IntegerField(null=True)
    

    def __str__(self):
        return self.nombre

class ImagenesProyecto(models.Model):
    imagen = CloudinaryField('imagen')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    