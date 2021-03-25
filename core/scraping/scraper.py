#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 08:32:48 2021

@author: nayannanara
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Scraping():
    url_dafiti = 'https://www.dafiti.com.br/bolsas-e-acessorios-femininos/bolsas/santa-lolla/?sort=popularity'
    url_zattini = 'https://www.zattini.com.br/refactoring/acessorios/feminino?mi=ztt_hm_fem_cat3_bolsaseacessorios&psn=Banner_BarradeCategorias_3fem&fc=barradecategorias&marca=santa-lolla&nsCat=Artificial&sort=relevance&tipo-de-produto=bolsas'
    all_products = []

    def scraping_dafiti():
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        
        # driver = webdriver.Chrome(executable_path='/home/nayannanara/automation-team-store-challenge/core/scraping/chromedriver', options=chrome_options)
        driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX
        )
        driver.get(Scraping.url_dafiti)
        sleep(3)
        
        ul_pag = driver.find_element_by_class_name('pagination-list').find_elements_by_tag_name('li')[-2].text
        num_page = []
        
        for pag in range(1,(int(ul_pag)+1)):
            num_page.append(pag)
        
        urls_dafiti = []   
        for x in num_page:
            url = f"{Scraping.url_dafiti}&page={x}"
            urls_dafiti.append(url)
        
        for url in urls_dafiti:
            driver.get(url)
            driver.execute_script('window.scrollBy(0, 300)')
            sleep(2)
            driver.execute_script('window.scrollBy(0, 600)')
            driver.execute_script('window.scrollBy(0, 900)')
            sleep(2)
            driver.execute_script('window.scrollBy(0, 1200)')
            driver.execute_script('window.scrollBy(0, 1500)')
            sleep(2)
            driver.execute_script('window.scrollBy(0, 1800)')
            driver.execute_script('window.scrollBy(0, 2100)')
            
            try:
                button = driver.find_element_by_xpath('//*[@id="dy_newsletter_submit"]/div[3]/button[2]').click()
            except:
                pass
            
            products = driver.find_elements_by_class_name('product-box')
            
            for product in products:
                div_detail = product.find_element_by_class_name('product-box-detail')
                marca = div_detail.find_element_by_class_name('product-box-brand').text
                descricao = div_detail.find_element_by_class_name('product-box-title').text
                div_precos = product.find_element_by_class_name('product-box-price')
                link_produto = product.find_element_by_class_name('product-box-link').get_attribute('href')
                link_img_produto = product.find_element_by_class_name('product-image').get_attribute('src')
                loja = 'Dafiti'
                
                try:
                    preco_original = div_precos.find_element_by_class_name('product-box-price-from').text
                except:
                    preco_original = 0.00
                try:
                    preco_promocional = div_precos.find_element_by_class_name('product-box-price-to').text     
                except:
                    preco_promocional = 0.00
                
                if preco_promocional != 0:    
                    tp_promocao = 'Oferta'
                else:
                    tp_promocao = 'Sem promoçao'
                
                product = {
                    'descricao': descricao,
                    'preco_original': preco_original,
                    'preco_promocional': preco_promocional,
                    'link_produto': link_produto,
                    'tp_promocao': tp_promocao,
                    'link_img_produto': link_img_produto,
                    'marca': marca,
                    'status': True,
                    'loja': loja
                }
        
                Scraping.all_products.append(product)
        return Scraping.all_products

    def scraping_zattini():
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        
        # driver = webdriver.Chrome(executable_path='/home/nayannanara/automation-team-store-challenge/core/scraping/chromedriver', options=chrome_options)
        driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX
        )
        driver.get(Scraping.url_zattini)
        sleep(3)
        
        ul_pag = driver.find_element_by_class_name('pagination').find_elements_by_tag_name('a')[-2].text
        num_page = []
        
        for pag in range(1,(int(ul_pag)+1)):
            num_page.append(pag)
        
        urls_zattini = []   
        for x in num_page:
            url = f"{Scraping.url_zattini}&page={x}"
            urls_zattini.append(url)
            
        for url in urls_zattini:
            driver.get(url)
            driver.execute_script('window.scrollBy(0, 300)')
            sleep(2)
            driver.execute_script('window.scrollBy(0, 600)')
            driver.execute_script('window.scrollBy(0, 900)')
            sleep(2)
            driver.execute_script('window.scrollBy(0, 1200)')
            driver.execute_script('window.scrollBy(0, 1500)')
            sleep(2)
            driver.execute_script('window.scrollBy(0, 1800)')
            driver.execute_script('window.scrollBy(0, 2100)')
        
            
            products = driver.find_elements_by_class_name('item-card')
            
            for product in products:
                descricao = product.find_element_by_class_name('item-card__description__product-name').text
                marca = product.find_element_by_xpath('//*[@id="content"]/section/section[2]/h1').text
                link_produto = product.find_element_by_class_name('item-card__images__image-link').get_attribute('href')
                link_img_produto = product.find_element_by_class_name('item-card__images__image-link').find_element_by_tag_name('img').get_attribute('src')
                loja = 'Zattini'
        
                try:
                    preco_original = product.find_element_by_class_name('pr')
                    preco_original = preco_original.find_element_by_tag_name('del').text
                except:
                    preco_original = 0.00 
        
                try:
                    preco_promocional = product.find_element_by_class_name('full-mounted-price')
                    preco_promocional = preco_promocional.find_element_by_class_name('haveInstallments').text
                except:
                    preco_promocional = 0.00
                    
                if preco_original != 0:    
                    tp_promocao = 'Oferta'
                else:
                    tp_promocao = 'Sem promoçao'
                    preco_original = preco_promocional
                    preco_promocional = 0.00
        
                product = {
                    'descricao': descricao,
                    'preco_original': preco_original,
                    'preco_promocional': preco_promocional,
                    'link_produto': link_produto,
                    'tp_promocao': tp_promocao,
                    'link_img_produto': link_img_produto,
                    'marca': marca,
                    'status': True,
                    'loja': loja
                }
                if preco_original !=0:   
                    Scraping.all_products.append(product)
        return Scraping.all_products


    def get_all_products():
        all_products = Scraping.scraping_zattini() + Scraping.scraping_dafiti()
        return all_products


    