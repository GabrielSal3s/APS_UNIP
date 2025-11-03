import os
import requests
import csv

def baixar_dados_inpe():
    """
    Baixa o arquivo CSV do INPE (últimos 10 minutos) e retorna uma lista com os valores da coluna 'frp'.
    """
    url = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/10min/focos_10min_20251103_1520.csv"
    os.makedirs("data", exist_ok=True)
    caminho = os.path.join("data", "focos_10min.csv")

    try:
        # Faz download do CSV
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ CSV baixado e salvo em: {caminho}")
    except Exception as e:
        print(f"⚠️ Erro ao baixar CSV: {e}")
        return [10, 5, 8, 3, 7]  # fallback

    # Lê coluna 'frp'
    frp_lista = []
    try:
        with open(caminho, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("frp") and row["frp"].isdigit():
                    frp_lista.append(int(row["frp"]))
        print(f"🔢 Total de valores 'frp' extraídos: {len(frp_lista)}")
    except Exception as e:
        print(f"⚠️ Erro ao ler CSV: {e}")
        return [10, 5, 8, 3, 7]

    return frp_lista[:1000] if frp_lista else [10, 5, 8, 3, 7]

def salvar_resultados(resultados):
    os.makedirs("data", exist_ok=True)
    caminho = os.path.join("data", "resultados.csv")
    cabecalho = ["algoritmo", "comparacoes", "tempo_exec"]
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho)
        writer.writeheader()
        writer.writerows(resultados)
    print(f"✅ Resultados salvos em: {caminho}")