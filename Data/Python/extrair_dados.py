import zipfile
import os

# Caminho para o arquivo zip e o destino de extração
zip_file = 'C:/Users/Dell/Desktop/USE/data_analytics_jr_test/Data/Data.zip'
extraction_path = 'C:/Users/Dell/Desktop/USE/data_analytics_jr_test/Data/'

# Abrir o arquivo zip e extrair seu conteúdo
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(extraction_path)

print("Dados extraídos com sucesso!")


