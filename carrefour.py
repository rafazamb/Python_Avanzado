# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:50:42 2023

@author: Administrator
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import sqlite3

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

# Accedemos a la web
driver.get('https://www.carrefour.es')

time.sleep(2)

# Aceptar cookies
driver.find_element('xpath', '//*[@id="onetrust-accept-btn-handler"]').click()

time.sleep(2)

# Buscar producto
driver.find_element('xpath', '//*[@id="search-input"]').click()

time.sleep(2)

driver.find_element('xpath', '//*[@id="empathy-x"]/header/div[1]/div/input[3]').send_keys('Leche Pascual')

time.sleep(2)

# Extraer el HTML
html = driver.page_source


soup = BeautifulSoup(html)
productos = soup.find_all('h1', class_='ebx-result-title ebx-result__title')
lista_productos = []

for producto in productos:
    lista_productos.append(producto.text)
    
precios = soup.find_all('strong', class_='ebx-result-price__value')
lista_precios = []
for precio in precios:
    lista_precios.append(precio.text)
    

fecha_hoy = datetime.today().strftime('%Y-%m-%d')

df = pd.DataFrame({'Fecha':[fecha_hoy]*len(lista_precios),
                  'Producto':lista_productos,
                  'Precio':lista_precios})


carrefour = sqlite3.connect('carrefour.sqlite')

df.to_sql('Pascual', con=carrefour, if_exists='append')

driver.quit()