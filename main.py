import requests
import os
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import re


cidade = input('Digite a cidade que voce deseja pesquisar: ') # usuario digita qual cidade deseja

options = Options()
options.add_argument('window-size=1650,1000')

navegador = webdriver.Chrome(options=options)

navegador.get('https://www.airbnb.com.br/')
sleep(4)

input_place2 = navegador.find_element(By.CLASS_NAME, "_160gnkxa") # Aceita o cookie
input_place2.click()
sleep(3)

input_place3 = navegador.find_element(By.CLASS_NAME, "f19g2zq0")  # Clica em 'Qualquer lugar'
input_place3.click()
sleep(3)

# procura o input, insere a cidade e pesquisa
input_place = navegador.find_element(By.CLASS_NAME, "iluujbk")
input_place.send_keys(cidade)    
sleep(2)
input_place.submit()
sleep(3)

dados_hospedagens = []

while True:
    page_content = navegador.page_source
    site = BeautifulSoup(page_content, 'html.parser') # Pega o conteúdo html

    hospedagens = site.findAll('div', attrs={'itemprop':'itemListElement'}) # Procura pelos itens
    for hospedagem in hospedagens:
        hospedagem_nome = hospedagem.find('div', attrs={'data-testid':'listing-card-title'})              # Captura o nome
        hospedagem_detalhes = hospedagem.findAll('div', attrs={'data-testid':'listing-card-subtitle'})    # Captura os detalhes
        hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})                               # Captura a url
        hospedagem_preco = hospedagem.find('div', attrs={'class':'_1jo4hgw'}).text                        # Captura o preco
        hospedagem_detalhes = ''.join([detalhe.text + ', ' for detalhe in hospedagem_detalhes])           # Faz um join de todos detalhes
        dados_hospedagens.append([hospedagem_nome.text, hospedagem_detalhes, hospedagem_url['content'], hospedagem_preco])

    button = navegador.find_element(By.CLASS_NAME, 'l1ovpqvx.c1ytbx3a') # clica no próximo
    desabilitado = button.get_attribute("disabled")

    if desabilitado: # caso o botão de próximo esteja desabilitado sai do for
        break

    button.click()
    sleep(4)
    
# cria o dataframe
dados = pd.DataFrame(dados_hospedagens, columns=['Nome', 'Detalhes', 'URL', 'Valor'])
data = datetime.datetime.now()
dia = data.day
mes = data.month
ano = data.year

# substitui os espaços por underline
cidade = cidade.replace(' ', '_')
caminho = os.path.join('dados-cidades', cidade)
nome_arquivo = f'({dia}-{mes}-{ano}).csv'

# se o caminho não existir, cria
if not os.path.exists(caminho):
    os.makedirs(caminho)

dados.to_csv(os.path.join(caminho, nome_arquivo), index=False)