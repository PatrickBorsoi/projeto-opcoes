#%%
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

extracao_de_planilhas()

datas = verifcar_dia()

data_atual = datas['dia_atual_formatado']


path_download = os.path.expanduser("~/Downloads")
path_pasta_opcoes = os.path.expanduser("C:/Users/Patrick/Desktop/workspace/pipeline_opcoes/data")
primeira_palavra = 'Opções'

mover_arquivos(path_downloads=path_download,path_pasta_padrao_dos_arquivos=path_pasta_opcoes, primeira_palavra=primeira_palavra)

df_total = ler_arquivos(path_pasta_padrao_dos_arquivos=path_pasta_opcoes)

remover_arquivos(path_pasta_padrao_dos_arquivos=path_pasta_opcoes, primeira_palavra=primeira_palavra)


df_total = transformacao(df=df_total)

tipo_do_arquivo = input('Digite o arquivo (csv ou xlsx)')

exportar_arquivo(df=df_total,data_atual=data_atual, path_database=path_pasta_opcoes,formato_do_arquivo=tipo_do_arquivo)


#transformação


