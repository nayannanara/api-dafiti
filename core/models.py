from model_utils.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from autoslug import AutoSlugField

class Produto(TimeStampedModel):
    descricao = models.CharField(_("Descrição do produto"), max_length=255, null=False, blank=False)
    preco_original =  models.DecimalField(_("Preço do produto"),max_digits=10, decimal_places=2)
    preco_promocional =  models.DecimalField(_("Preço promocional"),max_digits=10, decimal_places=2, default=0)
    promocao = models.BooleanField(default=False, verbose_name=_("Possui Promoção?"))
    link_produto = models.TextField()
    link_img_produto = models.TextField()
    slug = AutoSlugField(unique=True, always_update=False, populate_from="descricao")
    status = models.BooleanField(default=False, verbose_name=_("Ativo?"))
    marca = models.CharField(_("Marca"), max_length=25, null=False, blank=False)
    loja = models.CharField(_("Loja"), max_length=25, null=False, blank=False)
    qtd_vezes = models.IntegerField(_("Quantidade de vezes da mudança do preço"), default=0)


    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.descricao
    
    
class CompareProduto(TimeStampedModel):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="compare", null=True)
    preco_produto =  models.DecimalField(_("Preço do produto"),max_digits=10, decimal_places=2)
    loja = models.CharField(_("Loja"), max_length=25, null=False, blank=False)
    promocao = models.BooleanField(default=False, verbose_name=_("Possui Promoção?"))


    class Meta:
        verbose_name_plural = "Compare produtos"

    def __str__(self):
        return self.produto.descricao  
