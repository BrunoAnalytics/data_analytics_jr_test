import pandas as pd

# Caminhos para os arquivos
dicionario_escolas_path = 'C:/Users/Dell/Desktop/USE/data_analytics_jr_test/Data/Data/Escolas/dicionarioescolas.xlsx'
escolas_path = 'C:/Users/Dell/Desktop/USE/data_analytics_jr_test/Data/Data/Escolas/escolas-dez-2010.csv'
dicionario_perfil_path = 'C:/Users/Dell/Desktop/USE/data_analytics_jr_test/Data/Data/Perfil dos educandos/dicionariopefileducando.xlsx'
perfil_educando_path = 'C:/Users/Dell/Desktop/USE/data_analytics_jr_test/Data/Data/Perfil dos educandos/idadeserieneeracadez17.csv'

# Função para carregar arquivos CSV e exibir as primeiras 2 linhas
def carregar_e_exibir_csv(path, encoding='utf-8', delimiters=[',', ';']):
    for delimiter in delimiters:
        try:
            df = pd.read_csv(path, encoding=encoding, delimiter=delimiter)
            print(f"\nPrimeiras 2 linhas de {path} com delimitador '{delimiter}':")
            print(df.head(2))
            return df
        except Exception as e:
            print(f"Erro ao carregar {path} com delimitador '{delimiter}': {e}")
    return None

# Função para carregar arquivos Excel e exibir as primeiras 2 linhas
def carregar_e_exibir_excel(path):
    try:
        df = pd.read_excel(path)
        print(f"\nPrimeiras 2 linhas de {path}:")
        print(df.head(10))
        return df
    except Exception as e:
        print(f"Erro ao carregar {path}: {e}")
        return None

# Carregar os dados Excel (dicionários)
dicionario_escolas = carregar_e_exibir_excel(dicionario_escolas_path)
dicionario_perfil = carregar_e_exibir_excel(dicionario_perfil_path)

# Carregar os dados CSV com verificações de encoding e delimitadores
escolas = carregar_e_exibir_csv(escolas_path, encoding='utf-8')
if escolas is None:
    escolas = carregar_e_exibir_csv(escolas_path, encoding='ISO-8859-1')

perfil_educando = carregar_e_exibir_csv(perfil_educando_path, encoding='utf-8')
if perfil_educando is None:
    perfil_educando = carregar_e_exibir_csv(perfil_educando_path, encoding='ISO-8859-1')
