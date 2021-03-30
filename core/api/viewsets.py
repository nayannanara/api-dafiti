from core.models import Produto, CompareProduto, ContadorLoja
from core.api.filters import ProdutoFilterSet, CompareProdutoFilterSet
from .serializers import (
    ProdutoSerializer, 
    CompareProdutoListSerializer, 
    CompareProdutoSerializer, 
    PromocaoLojaSerializer,
    ComparacaoSerializer, 
    ConcorrenciaLojaSerializer
)
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.db.models import Count, Min, Max
import copy

class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    """
        Listagem de produtos
    """
    queryset = Produto.objects.all().order_by('id')
    serializer_class = ProdutoSerializer
    filter_class = ProdutoFilterSet

class CompareProdutoViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
        Compare preços entre os produtos
    """
    serializer_class = CompareProdutoSerializer

    def get_queryset(self):
        if self.request.session.get('lista') is None:
            self.request.session['lista'] = {}

        self.compare_list = self.request.session['lista']
        self.session = self.request.session
        session_key = self.request.session.session_key
        queryset = CompareProduto.objects.filter(session_key=session_key)
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
    
    def create(self, request, *args, **kwargs):

        if request.session.get('lista') is None:
            request.session['lista'] = {}

        self.compare_list = request.session['lista']
        self.session = request.session

        data = request.data.copy()
        produto = data['produto']

        queryset = Produto.objects.get(pk=produto)
        preco_produto = queryset.preco_original
        preco_promocional = queryset.preco_promocional
        loja = queryset.loja

        if preco_promocional != 0:
            preco_produto = preco_promocional
            promocao = True
        else:
            preco_produto = preco_produto
            promocao = False

        data['session_key'] = self.session.session_key
        data['preco_produto'] = preco_produto
        data['promocao'] = promocao
        data['loja'] = loja

        serializer = CompareProdutoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PromocaoLojaViewSet(viewsets.ReadOnlyModelViewSet):
    """
        Qual loja tem mais promoção
    """
    serializer_class = PromocaoLojaSerializer
    
    def get_queryset(self):
        queryset = Produto.objects.values('loja').filter(promocao=True).order_by().annotate(quantidade_promo=Count('loja'))
        return queryset


class ComparacaoViewSet(viewsets.ReadOnlyModelViewSet):
    """
        Comparação de produtos escolhidos
    """
    serializer_class = ComparacaoSerializer

    def get_queryset(self):
        session_key = self.request.session.session_key
        queryset = CompareProduto.objects.raw(
            f'''select loja, MIN(preco_produto) OVER (PARTITION BY preco_produto), promocao, produto_id, id
            from core_compareproduto
            where session_key = '{session_key}'
            order by promocao asc limit 1'''
            )
        CompareProduto.objects.filter(session_key=session_key).update(comparado=True)
        try:
            for dado in queryset: dado.loja
            ConcorrenciaLojaViewSet.contador_loja(dado.loja)
            self.request.session.flush()
        except:
            return queryset
        return queryset 

class ConcorrenciaLojaViewSet(viewsets.ReadOnlyModelViewSet):        
    """
        Listagem de concorrência entre as lojas
    """

    queryset = ContadorLoja.objects.all().order_by('id')
    serializer_class = ConcorrenciaLojaSerializer

    def contador_loja(loja):
        data = ContadorLoja.objects.filter(loja=loja).values('loja', 'qtd_vezes')

        if data.exists():
            qtd_vezes = data[0]['qtd_vezes'] + 1
            data.update(qtd_vezes=qtd_vezes)
        else:
            ContadorLoja.objects.create(loja=loja, qtd_vezes=1)

    