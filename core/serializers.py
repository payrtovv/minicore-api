from rest_framework import serializers
from .models import Venta, Vendedor


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ["id", "Vendedor", "fecha", "cantidad"]
        read_only_fields = ["fecha"]

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que 0")
        return value
    

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ["id", "Nombre"]