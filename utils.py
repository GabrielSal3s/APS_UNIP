import os
import requests
import csv
import zipfile

def baixar_e_extrair_zip(url):
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_zip = os.path.join(pasta_atual, "dados.zip")
    caminho_csv = None

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        with open(caminho_zip, "wb") as f:
            f.write(response.content)
        print(f"✅ ZIP baixado em: {caminho_zip}")
    except Exception as e:
        print(f"⚠️ Erro ao baixar ZIP: {e}")
        return None

    try:
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(pasta_atual)
            for file_name in zip_ref.namelist():
                if file_name.endswith(".csv"):
                    caminho_csv = os.path.join(pasta_atual, file_name)
                    break
        print(f"📂 CSV extraído: {caminho_csv}")
    except Exception as e:
        print(f"⚠️ Erro ao extrair ZIP: {e}")
        return None

    return caminho_csv

def ler_coluna_frp(caminho_csv):
    frp_lista = []
    try:
        with open(caminho_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                valor = row.get("frp")
                if valor:
                    try:
                        frp_lista.append(float(valor))
                    except ValueError:
                        continue
        print(f"🔢 Total de valores 'frp' extraídos: {len(frp_lista)}")
    except Exception as e:
        print(f"⚠️ Erro ao ler CSV: {e}")
    return frp_lista