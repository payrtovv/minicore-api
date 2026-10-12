from django.db import models

# Create your models here.


class Vendedor(models.Model):
    Nombre = models.CharField(max_length=100)
    

class Venta(models.Model):
    Vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE
    )
    
    fecha = models.DateField(auto_now_add=True)
    
    cantidad = models.FloatField()
    