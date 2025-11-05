# utils.py
# -------------------------------------------------------
# Funções utilitárias para o projeto APS de ordenação:
# - Obtenção de URLs de arquivos do INPE
# - Download e extração de arquivos ZIP
# - Leitura de dados CSV
# -------------------------------------------------------

import os
import requests
import csv
import zipfile
from bs4 import BeautifulSoup


def obter_urls_recentes():
    """Obtém os dois arquivos ZIP mais recentes disponíveis no site do INPE."""
    base_url = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/EstadosBr_sat_ref/RJ/"
    try:
        response = requests.get(base_url, verify=False, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Filtra apenas links que terminam em .zip
        links = [a["href"] for a in soup.find_all("a") if a["href"].endswith(".zip")]
        links.sort(reverse=True)  # Organiza para pegar os mais recentes
        ultimos = links[:2]
        urls = [base_url + link for link in ultimos]

        print(f"🔗 Arquivos identificados: {len(urls)} encontrados.\n")
        return urls
    except Exception as e:
        print(f"⚠️ Erro ao obter lista de arquivos: {e}")
        return []


def baixar_e_extrair_zip(url):
    """Baixa um arquivo ZIP do servidor e extrai o CSV contido nele."""
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_zip = os.path.join(pasta_atual, "dados.zip")
    caminho_csv = None

    try:
        response = requests.get(url, timeout=15, verify=False)
        response.raise_for_status()
        with open(caminho_zip, "wb") as f:
            f.write(response.content)
        print("✅ Download concluído.")
    except Exception as e:
        print(f"⚠️ Erro ao baixar ZIP: {e}")
        return None

    # Extrai o CSV de dentro do ZIP
    try:
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(pasta_atual)
            for file_name in zip_ref.namelist():
                if file_name.endswith(".csv"):
                    caminho_csv = os.path.join(pasta_atual, file_name)
                    break
        print(f"📂 Arquivo CSV extraído com sucesso: {caminho_csv}\n")
    except Exception as e:
        print(f"⚠️ Erro ao extrair ZIP: {e}")
        return None

    return caminho_csv


def ler_dados(caminho_csv):
    """Lê o arquivo CSV e retorna uma lista de dicionários com os dados."""
    registros = []
    try:
        with open(caminho_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")

            # Caso o delimitador não seja tabulação, tenta vírgula
            if len(reader.fieldnames) == 1:
                f.seek(0)
                reader = csv.DictReader(f, delimiter=",")

            registros = list(reader)
        print(f"📊 Registros carregados: {len(registros)}")
        print(f"🧩 Cabeçalhos detectados: {reader.fieldnames}\n")
    except Exception as e:
        print(f"⚠️ Erro ao ler CSV: {e}")
    return registros