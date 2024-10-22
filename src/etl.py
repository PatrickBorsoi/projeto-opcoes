#%%
import pandas as pd
import os
import glob
import shutil
from datetime import datetime, timedelta
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
    arquivos_excel = glob.glob(os.path.join(path_pasta_padrao_dos_arquivos, '*.xlsx'))
    df_list: list = [pd.read_excel(arquivo,skiprows=1,engine='openpyxl') for arquivo in arquivos_excel]
    df_tabela_total: list = pd.concat(df_list, ignore_index=True)
    df_tabela_total = pd.DataFrame(df_tabela_total)
    df_tabela_total.columns= df_tabela_total.columns.str.strip()
    # df_tabela_total['Strike'] = df_tabela_total['Strike'].combine_first(df_tabela_total['Strike'])
    df_tabela_total['Strike'] = df_tabela_total['Strike']


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
