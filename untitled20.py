# -*- coding: utf-8 -*-
"""Untitled20.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16ozDKbLR_7Pb8LCfZJLjTY85ov1kL61J

User
# Módulo 5 Tarefa 1
## Base de nascidos vivos do DataSUS
O DataSUS disponibiliza diversos arquivos de dados com relação a seus segurados, conforme a [lei da transparência de informações públicas](https://www.sisgov.com/transparencia-acesso-informacao/#:~:text=A%20Lei%20da%20Transpar%C3%AAncia%20(LC,em%20um%20site%20na%20internet.).

Essas informações podem ser obtidas pela internet [aqui](http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1). Como o processo de obtenção desses arquivos foge um pouco do nosso escopo, deixamos o arquivo ```SINASC_RO_2019.csv``` já como vai ser encontrado no DataSUS. O dicionário de dados está no arquivo ```estrutura_sinasc_para_CD.pdf``` (o nome do arquivo tal qual no portal do DataSUS).

### Nosso objetivo
Queremos deixar uma base organizada para podermos estudar a relação entre partos com risco para o bebê e algumas condições como tempo de parto, consultas de pré-natal etc.
"""

import pandas as pd
import requests

# 1) seu código aqui
sinasc = pd.read_csv('SINASC_RO_2019.csv')
print(sinasc.shape)
sinasc.drop_duplicates().shape
# Não há duplicados

# Passo 1: Carregar a base e verificar duplicatas
sinasc_df = pd.read_csv('SINASC_RO_2019.csv')
num_total_registros = len(sinasc_df)
num_registros_nao_duplicados = sinasc_df.drop_duplicates().shape[0]
print(f"Número total de registros: {num_total_registros}")
print(f"Número de registros não duplicados: {num_registros_nao_duplicados}")
print(f"Há linhas duplicadas? {'Sim' if num_total_registros != num_registros_nao_duplicados else 'Não'}")

# Passo 2: Contar valores missing por variável
missing_por_variavel = sinasc_df.isnull().sum()
print("\nNúmero de valores missing por variável:")
print(missing_por_variavel)

# Passo 3: Selecionar colunas de interesse e contar valores missing novamente
colunas_interesse = ['LOCNASC', 'IDADEMAE', 'ESTCIVMAE', 'ESCMAE', 'QTDFILVIVO', 'GESTACAO', 'GRAVIDEZ', 'CONSULTAS', 'APGAR5']
sinasc_selecionado = sinasc_df[colunas_interesse]
missing_selecionado = sinasc_selecionado.isnull().sum()
print("\nNúmero de valores missing nas colunas selecionadas:")
print(missing_selecionado)

# Passo 4: Remover registros com Apgar5 não preenchido e contar novamente os missings
sinasc_selecionado = sinasc_selecionado.dropna(subset=['APGAR5'])
missing_apgar5_removido = sinasc_selecionado.isnull().sum()
print("\nApós remover registros com Apgar5 não preenchido:")
print("Número de linhas:", sinasc_selecionado.shape[0])
print("Número de valores missing nas colunas selecionadas:")
print(missing_apgar5_removido)

# Passo 5 e 6: Substituir valores '9' por NaN e tratar QTDFILVIVO
sinasc_selecionado.replace({'ESTCIVMAE': 9, 'CONSULTAS': 9}, pd.NA, inplace=True)
sinasc_selecionado['QTDFILVIVO'].fillna(0, inplace=True)

# Passo 7: Preencher valores faltantes de outras variáveis (escolha do cientista)
# Vamos assumir que valores faltantes em GESTACAO, GRAVIDEZ e ESCMAE serão substituídos por 'Não Preenchido'.
sinasc_selecionado[['GESTACAO', 'GRAVIDEZ', 'ESCMAE']] = sinasc_selecionado[['GESTACAO', 'GRAVIDEZ', 'ESCMAE']].fillna('Não Preenchido')

# Passo 8: Criar categorização da variável Apgar5
def categorizar_apgar5(apgar5):
    if 8 <= apgar5 <= 10:
        return 'Normal'
    elif 6 <= apgar5 <= 7:
        return 'Asfixia Leve'
    elif 4 <= apgar5 <= 5:
        return 'Asfixia Moderada'
    elif 0 <= apgar5 <= 3:
        return 'Asfixia Severa'
    else:
        return pd.NA

sinasc_selecionado['APGAR5_CATEGORIA'] = sinasc_selecionado['APGAR5'].apply(categorizar_apgar5)

# Passo 8 (continuação): Calcular frequências da categorização
frequencias_apgar5 = sinasc_selecionado['APGAR5_CATEGORIA'].value_counts()
print("\nFrequências da categorização de Apgar5:")
print(frequencias_apgar5)

# Passo 9: Renomear as variáveis para snake case
sinasc_selecionado.columns = sinasc_selecionado.columns.str.lower().str.replace(' ', '_')

# Exibir as primeiras linhas do DataFrame resultante
print("\nDataFrame resultante:")
print(sinasc_selecionado.head())