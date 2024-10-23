#%%
import pandas as pd
import os
import glob
import shutil
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time


def verifcar_dia():
    data = datetime.now()
    data_formatada = data.strftime("%d-%m-%Y")
    return  {
        'dia_atual' : data,
        'dia_atual_formatado' : data_formatada
    }

def mover_arquivos(path_downloads: str, path_pasta_padrao_dos_arquivos: str, primeira_palavra: str):
    arquivos = [arquivo for arquivo in os.listdir(path_downloads) if arquivo.startswith(primeira_palavra)]
    for arquivo in arquivos:
        path_arquivo = os.path.join(path_downloads, arquivo)
        shutil.move(path_arquivo, path_pasta_padrao_dos_arquivos)


def ler_arquivos(path_pasta_padrao_dos_arquivos: str) -> pd.DataFrame:
    # Buscar todos os arquivos Excel na pasta
    arquivos_excel = glob.glob(os.path.join(path_pasta_padrao_dos_arquivos, '*.xlsx'))
    
    # Ler todos os arquivos Excel e armazenar em uma lista de DataFrames
    df_list = [pd.read_excel(arquivo, skiprows=1, engine='openpyxl') for arquivo in arquivos_excel]
    
    # Concatenar todos os DataFrames em um único DataFrame
    df_tabela_total = pd.concat(df_list, ignore_index=True)
    
    df_tabela_total.columns = df_tabela_total.columns.str.strip()
        
    cols = pd.Series(df_tabela_total.columns)
    for dup in cols[cols.duplicated()].unique():  # Identifica colunas duplicadas
        cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]
    df_tabela_total.columns = cols

    df_tabela_total['Strike_Unificado'] = df_tabela_total['Strike'].combine_first(df_tabela_total['Strike_1'])
    df_tabela_total = df_tabela_total.drop(columns=['Strike', 'Strike_1'])
    print(df_tabela_total)
    
    return df_tabela_total



def remover_arquivos(path_pasta_padrao_dos_arquivos: str, primeira_palavra):
    arquivos_excel = glob.glob(os.path.join(path_pasta_padrao_dos_arquivos, '*.xlsx'))
    for arquivo in arquivos_excel:
        if arquivo.startswith(primeira_palavra):
            continue
        os.remove(arquivo)

def exportar_arquivo(path_database: str,df: pd.DataFrame, formato_do_arquivo: str, data_atual: datetime) ->str:
    for formato in formato_do_arquivo:
        if formato == "csv":
            df.to_csv(f'{path_database}/{data_atual}_arquivo todas opções.csv')
            return 'Arquivo exportado com sucesso'
        elif formato == "xlsx" or "excel":
            df.to_excel(f'{path_database}/{data_atual}_arquivo todas opções.xlsx',index=False)
        else:
            return 'Digite o formato de arquivo certo'


# Funções de transformaçã
# %%
def transformacao(df: pd.DataFrame):
        # Remover colunas do dataframe
    colunas_para_remover = ['F.M.', 'A/I/OTM']
    df_final = df.drop(columns=colunas_para_remover)

    # Remova as linhas onde a coluna 'Mod.' é igual a 'A'
    df_final = df_final[df_final['Mod.'] != 'A']

    # Remova as linhas onde a coluna 'Núm. de Neg.' é menor que 50
    df_final = df_final[df_final['Núm. de Neg.'] >= 50]
    return df_final


def extracao_de_planilhas():
    driver = webdriver.Chrome()
    driver.get('https://opcoes.net.br/opcoes/bovespa')
    opcoes: list = driver.find_elements(By.XPATH, '//*[@id="grade-opcoes"]/div[1]/div[1]/select[2]/option')

    lista_de_ativos: list = []

    for nome_ativo in opcoes[1:]:
        time.sleep(1)
        nome_ativo.click()
        lista_de_ativos.append(nome_ativo.text)
        time.sleep(2)
        botao_exportar_para_excel = driver.find_element(By.XPATH, '//*[@id="tblListaOpc_wrapper"]/div[1]/div[2]/div/button[2]')
        time.sleep(1)
        botao_exportar_para_excel.click()

    driver.quit()