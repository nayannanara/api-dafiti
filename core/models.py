from model_utils.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from autoslug import AutoSlugField

class Produto(TimeStampedModel):
    descricao = models.CharField(_("Descrição do produto"), max_length=255, null=False, blank=False)
    preco_original =  models.DecimalField(_("Preço do produto"),max_digits=10, decimal_places=2)
    preco_promocional =  models.DecimalField(_("Preço promocional"),max_digits=10, decimal_places=2, default=0)
    tp_promocao = models.CharField(_("Tipo de promoção"), max_length=100, null=False, blank=False)
    link_produto = models.CharField(_("Link do produto"), max_length=255, null=True, blank=True)
    link_img_produto = models.CharField(_("Link da imagem do produto"), max_length=255, null=True, blank=True)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="descricao")
    status = models.BooleanField(default=False, verbose_name=_("Ativo?"))
    marca = models.CharField(_("Marca"), max_length=25, null=False, blank=False)
    loja = models.CharField(_("Loja"), max_length=25, null=False, blank=False)


    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.descricao
