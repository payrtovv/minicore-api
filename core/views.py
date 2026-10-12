from datetime import date
from decimal import Decimal

from django.db.models import Sum, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Venta, Vendedor
from .services import calculate_commission      


@api_view(["GET"])
def comisiones_view(request):
    desde = request.query_params.get("desde")
    hasta = request.query_params.get("hasta")

    if not desde or not hasta:
        return Response(
            {"error": "Debes enviar 'desde' y 'hasta' (formato YYYY-MM-DD)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        fecha_desde = date.fromisoformat(desde)
        fecha_hasta = date.fromisoformat(hasta)
    except ValueError:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
        )

    if fecha_desde > fecha_hasta:
        return Response(
            {"error": "'desde' no puede ser mayor que 'hasta'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    resumen = (
        Venta.objects
        .filter(fecha__range=(fecha_desde, fecha_hasta))
        .values("Vendedor__id", "Vendedor__Nombre")
        .annotate(total=Sum("cantidad"), num_ventas=Count("id"))
    )

    resultados = []
    for fila in resumen:
        total = Decimal(str(fila["total"]))
        rate, comision = calculate_commission(total)
        resultados.append({
            "vendedor_id": fila["Vendedor__id"],
            "vendedor": fila["Vendedor__Nombre"],
            "num_ventas": fila["num_ventas"],
            "total_ventas": str(total.quantize(Decimal("0.01"))),
            "porcentaje": str(rate * 100),
            "comision": str(comision),
        })

    return Response({
        "resultados": resultados,
    })
    
from .serializers import VentaSerializer


@api_view(["POST"])
def crear_venta_view(request):
    serializer = VentaSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

from .serializers import VendedorSerializer


@api_view(["GET"])
def listar_vendedores_view(request):
    vendedores = Vendedor.objects.order_by("Nombre")
    return Response(VendedorSerializer(vendedores, many=True).data)