from django_filters import rest_framework as filters
from core.models import Produto, CompareProduto

class ProdutoFilterSet(filters.FilterSet):
    descricao = filters.CharFilter(
        field_name="descricao", lookup_expr="icontains"
    )
    
    loja = filters.CharFilter(
        field_name="loja", lookup_expr="icontains"
    )
    class Meta:
        model = Produto
        fields = ["descricao", "loja"]
        
class CompareProdutoFilterSet(filters.FilterSet):
    produto = filters.CharFilter(
        field_name="produto__descricao", lookup_expr="icontains"
    )
    
    loja = filters.CharFilter(
        field_name="loja", lookup_expr="icontains"
    )
    class Meta:
        model = CompareProduto
        fields = ["produto", "loja", "promocao"]        