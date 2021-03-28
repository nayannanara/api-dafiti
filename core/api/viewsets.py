from core.models import Produto, CompareProduto
from core.api.filters import ProdutoFilterSet, CompareProdutoFilterSet
from django.shortcuts import get_object_or_404
from .serializers import ProdutoSerializer, CompareProdutoListSerializer, CompareProdutoSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response

class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    """
        Listagem de produtos
    """
    queryset = Produto.objects.all().order_by('id')
    serializer_class = ProdutoSerializer
    filter_class = ProdutoFilterSet

class CompareProdutoViewSet(viewsets.ModelViewSet):
    """
        Comparação de preços entre os produtos
    """
    serializer_class = CompareProdutoSerializer
    filter_class = CompareProdutoFilterSet

    def get_queryset(self):
        queryset = CompareProduto.objects.all()
        return queryset

    def get_serializer_class(self):
        serializer_map = {
            "update": CompareProdutoSerializer,
            "partial_update": CompareProdutoSerializer,
            "create": CompareProdutoSerializer,
            "list": CompareProdutoListSerializer,
            "retrieve": CompareProdutoListSerializer
        }
        return serializer_map.get(self.action, super().get_serializer_class())
    