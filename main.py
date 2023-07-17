import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import re

options = Options()

options.add_argument('window-size=900,800')

navegador = webdriver.Chrome(options=options)

navegador.get('https://www.airbnb.com.br/')

sleep(3)

input_place2 = navegador.find_element(By.CLASS_NAME, "_160gnkxa")
input_place2.click()

sleep(3)

input_place3 = navegador.find_element(By.CLASS_NAME, "f19g2zq0")
input_place3.click()

sleep(3)

input_place = navegador.find_element(By.CLASS_NAME, "iluujbk")
input_place.send_keys('Luminárias')
input_place.submit()

sleep(3)



page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')

hospedagem = site.find('div', attrs={'itemprop':'itemListElement'})

print(hospedagem.prettify())

hospedagem_nome = hospedagem.find('meta', attrs={'itemprop': 'name'})
hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})
print('Nome:', hospedagem_nome['content'])
print('URL:', hospedagem_url['content'])

hospedagem_detalhes = hospedagem.find('span', attrs={'class':'a8jt5op'})
valor_por_noite = hospedagem_detalhes.text

valor_numérico = re.search(r'\d+', valor_por_noite).group()

print('Valor por noite: R$', valor_numérico)