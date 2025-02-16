import os
import pandas as pd
import time
from sqlalchemy import create_engine

# Defina as credenciais de acesso ao banco PostgreSQL
db_host = 'localhost'
db_name = 'postgres'
db_user = 'postgres'
db_password = 'bruno1234'
db_port = '5433'

# Conectar ao banco de dados PostgreSQL usando SQLAlchemy
connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)

# Definição das colunas corretas para os arquivos CSV
COLUMNS_ESCOLAS = [
    "DRE", "CODESC", "TIPOESC", "NOMES", "NOMESCOFI", "CEU", "DIRETORIA", "SUBPREF", "ENDERECO",
    "NUMERO", "BAIRRO", "CEP", "TEL1", "TEL2", "FAX", "SITUACAO", "CODDIST", "DISTRITO", "SETOR",
    "CODINEP", "CD_CIE", "EH", "FX_ETARIA", "DT_CRIACAO", "ATO_CRIACAO", "DOM_CRIACAO", "DT_INI_CONV",
    "DT_AUTORIZA", "DT_EXTINCAO", "NOME_ANT", "REDE", "LATITUDE", "LONGITUDE", "DATABASE"
]

COLUMNS_IDADE = [
    "dre", "codes", "tipoesc", "nomesc", "distrito", "setor", "ano", "rede", "modal", "descserie",
    "periodo", "turno", "descturno", "sexo", "idade", "nee", "raca", "qtd", "database"
]

# Função para converter a codificação para UTF-8
def convert_to_utf8(df):
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: str(x).encode('latin1', 'ignore').decode('utf-8', 'ignore') if isinstance(x, str) else x)
    return df

# Função para carregar e combinar arquivos CSV, mantendo apenas as colunas corretas
def load_and_combine_csvs(folder, expected_columns):
    combined_df = pd.DataFrame()
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path, delimiter=';', encoding='latin1')
                df = convert_to_utf8(df)

                # Manter apenas as colunas corretas
                df = df[[col for col in expected_columns if col in df.columns]]

                # Adicionar colunas ausentes como vazias
                for col in expected_columns:
                    if col not in df.columns:
                        df[col] = None

                df = df[expected_columns]  # Garantir a ordem das colunas
                combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df

# Função para carregar um único arquivo XLSX
def load_xlsx(file_path):
    df = pd.read_excel(file_path)
    df = convert_to_utf8(df)
    return df

# Função para importar os dados para o PostgreSQL
def load_combined_data_to_postgresql():
    chunksize = 50000
    
    # Diretórios de dados
    base_folder = 'C:/Users/Dell/Desktop/USE/data_analytics_jr_test/Data/Data'
    escolas_folder = os.path.join(base_folder, 'Escolas')
    perfil_folder = os.path.join(base_folder, 'Perfil dos educandos')

    # Processar arquivos CSV da pasta "Escolas"
    start_time = time.time()
    escolas_df = load_and_combine_csvs(escolas_folder, COLUMNS_ESCOLAS)
    schema_escolas = 'Escolas'
    table_escolas = 'dados_escolas'
    
    with engine.begin() as connection:
        for start in range(0, len(escolas_df), chunksize):
            chunk = escolas_df.iloc[start:start+chunksize]
            chunk.to_sql(table_escolas, connection, if_exists='append', index=False, schema=schema_escolas, chunksize=chunksize)
            print(f"Carregando pedaço {start} até {start+chunksize} de CSV (Escolas)...")
    
    print(f"Dados de Escolas importados para o esquema {schema_escolas}!")
    print(f"Tempo total para Escolas: {time.time() - start_time:.2f} segundos | Total de registros: {len(escolas_df)}")

    # Importar arquivo XLSX da pasta "Escolas"
    escolas_xlsx_path = os.path.join(escolas_folder, 'dicionarioescolas.xlsx')
    if os.path.exists(escolas_xlsx_path):
        escolas_xlsx_df = load_xlsx(escolas_xlsx_path)
        with engine.begin() as connection:
            escolas_xlsx_df.to_sql('dicionario_escolas', connection, if_exists='append', index=False, schema=schema_escolas)
            print("Dicionário XLSX (Escolas) importado com sucesso!")

    # Processar arquivos CSV da pasta "Perfil dos educandos"
    start_time = time.time()
    idade_df = load_and_combine_csvs(perfil_folder, COLUMNS_IDADE)
    schema_idade = 'Perfil dos educandos'
    table_idade = 'dados_idade'
    
    with engine.begin() as connection:
        for start in range(0, len(idade_df), chunksize):
            chunk = idade_df.iloc[start:start+chunksize]
            chunk.to_sql(table_idade, connection, if_exists='append', index=False, schema=schema_idade, chunksize=chunksize)
            print(f"Carregando pedaço {start} até {start+chunksize} de CSV (Idade)...")
    
    print(f"Dados de Idade importados para o esquema {schema_idade}!")
    print(f"Tempo total para Idade: {time.time() - start_time:.2f} segundos | Total de registros: {len(idade_df)}")

    # Importar arquivo XLSX da pasta "Perfil dos educandos"
    idade_xlsx_path = os.path.join(perfil_folder, 'dicionariopefileducando.xlsx')
    if os.path.exists(idade_xlsx_path):
        idade_xlsx_df = load_xlsx(idade_xlsx_path)
        with engine.begin() as connection:
            idade_xlsx_df.to_sql('dicionario_idade', connection, if_exists='append', index=False, schema=schema_idade)
            print("Dicionário XLSX (Idade) importado com sucesso!")

# Executar a importação
load_combined_data_to_postgresql()
