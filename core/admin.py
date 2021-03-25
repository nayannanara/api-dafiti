from django.contrib import admin
from .models import Produto
# Register your models here.

class ProdutoAdmin(admin.ModelAdmin):
    # search_fields = ('nome', 'descricao','preco')
    list_display = ('descricao', 'preco_original','preco_promocional', 'tp_promocao', 'loja')
    list_filter = ['created']
    list_per_page = 30

admin.site.register(Produto, ProdutoAdmin)    