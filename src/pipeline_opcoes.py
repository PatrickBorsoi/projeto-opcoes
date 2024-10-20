from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import time
import shutil
import glob
import os
from etl import *
from bs4 import BeautifulSoup
import requests

driver = webdriver.Chrome()
driver.get('https://opcoes.net.br/opcoes/bovespa')
opcoes: list = driver.find_elements(By.XPATH, '//*[@id="grade-opcoes"]/div[1]/div[1]/select[2]/option')

lista_de_ativos: list = []

for nome_ativo in opcoes[1:5]:
    time.sleep(1)
    nome_ativo.click()
    lista_de_ativos.append(nome_ativo.text)
    time.sleep(2)
    botao_exportar_para_excel = driver.find_element(By.XPATH, '//*[@id="tblListaOpc_wrapper"]/div[1]/div[2]/div/button[2]')
    time.sleep(1)
    botao_exportar_para_excel.click()


datas = verifcar_dia()

data_atual = datas['dia_atual_formatado']


path_download = os.path.expanduser("~/Downloads")
path_pasta_opcoes = os.path.expanduser("C:/Users/Patrick/Desktop/workspace/pipeline_opcoes/data")
primeira_palavra = 'Opções'

mover_arquivos(path_downloads=path_download,path_pasta_padrao_dos_arquivos=path_pasta_opcoes, primeira_palavra=primeira_palavra)

df_total = ler_arquivos(path_pasta_padrao_dos_arquivos=path_pasta_opcoes)
print(df_total.columns)
print(df_total)

remover_arquivos(path_pasta_padrao_dos_arquivos=path_pasta_opcoes, primeira_palavra=primeira_palavra)

tipo_do_arquivo = input('Digite o arquivo (csv ou xlsx)')

exportar_arquivo(df=df_total,data_atual=data_atual, path_database=path_pasta_opcoes,formato_do_arquivo=tipo_do_arquivo)


#transformação

# %%
