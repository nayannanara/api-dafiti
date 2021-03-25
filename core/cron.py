from core.scraping.scraper import Scraping as scraper
from core.models import Produto

import re

def scraping():
    all_results = scraper.get_all_products()

    for result in all_results:
        preco_original = re.sub('[^0-9]', '', result["preco_original"])
        preco_original = float(int(preco_original)/100)

        if result["preco_promocional"] != 0.0:
            preco_promocional = re.sub('[^0-9]', '', result["preco_promocional"])
            preco_promocional = float(int(preco_promocional)/100)
        else:
            preco_promocional = result["preco_promocional"]


        verifica_prod = Produto.objects.filter(descricao=result["descricao"], loja=result["loja"]).exists()

        if not verifica_prod:
            Produto.objects.create(
                descricao=result["descricao"],
                preco_original=preco_original,
                preco_promocional=preco_promocional,
                tp_promocao=result["tp_promocao"],
                link_produto=result["link_produto"],
                link_img_produto=result["link_img_produto"],
                status=result["status"],
                loja=result["loja"],
                marca=result["marca"]
            )
            print('Produto registrado')
        else:
            queryset =  Produto.objects.get(descricao=result["descricao"],loja=result["loja"])
            preco = float(queryset.preco_original)
            preco_promo = float(queryset.preco_promocional)
            link_img_produto = queryset.link_img_produto
            status = queryset.status
            
            if preco != preco_original and result['tp_promocao'] == 'Oferta' and result['status']==True :
                Produto.objects.filter(descricao=result["descricao"],loja=result["loja"]).update(
                    preco_original=preco_original, tp_promocao=result['tp_promocao'], link_img_produto=result['link_img_produto'],
                    status=result['status']
                )
                print ('Produto está em promoção')

            if preco != preco_original and result['tp_promocao'] == 'Sem promoção' and result['status']==True:
                Produto.objects.filter(descricao=result["descricao"],loja=result["loja"]).update(
                    preco_original=preco_original, tp_promocao=result['tp_promocao'], preco_promocional=0.00, 
                    link_img_produto=result['link_img_produto'],
                    status=result['status']
                )
                print ('Produto não está em promoção')
            if link_img_produto != result['link_img_produto'] and result['status']==True:
                Produto.objects.filter(descricao=result["descricao"],
                loja=result["loja"]).update(link_img_produto=result['link_img_produto'],status=result['status'])

                print('Link da imagem do produto mudou')

            if result['status']==True:
                Produto.objects.filter(descricao=result["descricao"],
                loja=result["loja"]).update(status=result['status'])

                print('Produto disponivel')

    print('Produtos adicionados')