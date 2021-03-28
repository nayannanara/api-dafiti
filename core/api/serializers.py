from rest_framework import serializers
from core.models import Produto, CompareProduto

class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = ("id","descricao", "preco_original", "preco_promocional", "promocao", "marca", "loja", "status", "link_produto")
        

class CompareProdutoListSerializer(serializers.ModelSerializer):
    
    produto = ProdutoSerializer(many=True, read_only=True)
    
    class Meta:
        model = CompareProduto
        fields = ("id","produto", "preco_produto", "loja", "promocao")        

class CompareProdutoSerializer(serializers.ModelSerializer):
    
    # def create(self, validated_data):
    #     "Cria um historico para um dada previsao e atualiza o ´pm_atual` desse previsao"
    #     instance = super().create(validated_data)

    #     previsao = validated_data["previsao"]

    #     if not previsao.historicos.exists():
    #         self.save_previsao(previsao, validated_data)
    #         return instance

    #     if validated_data["date"] > previsao.dt_ultimo_pm:
    #         self.save_previsao(previsao, validated_data)
    #         return instance
    #     return instance
    
    class Meta:
        model = CompareProduto
        fields = "__all__"              