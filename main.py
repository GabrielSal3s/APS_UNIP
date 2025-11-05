import os
import csv
import zipfile
import requests
from algoritmos import bubble_sort, quick_sort  # Importa os algoritmos criados separadamente

def baixar_e_extrair_csv(url, pasta_destino):
    """Baixa e extrai um arquivo CSV de um ZIP remoto."""
    nome_zip = os.path.join(pasta_destino, url.split("/")[-1])
    nome_csv = nome_zip.replace(".zip", ".csv")

    # Baixa apenas se ainda não existir
    if not os.path.exists(nome_csv):
        print(f"📦 Baixando e processando: {url}")
        resposta = requests.get(url, verify=False)
        with open(nome_zip, "wb") as f:
            f.write(resposta.content)

        # Extrai o conteúdo e remove o ZIP
        with zipfile.ZipFile(nome_zip, "r") as zip_ref:
            zip_ref.extractall(pasta_destino)
        os.remove(nome_zip)
    else:
        print(f"📂 CSV existente: {nome_csv}")
    return nome_csv


def carregar_dados(caminho_csv):
    """Carrega os dados do CSV e corrige cabeçalhos com erros de formatação."""
    with open(caminho_csv, newline='', encoding="utf-8") as csvfile:
        leitor = csv.DictReader(csvfile)
        # Normaliza os nomes das colunas
        leitor.fieldnames = [h.strip().lower().replace(" ", "_").replace("í", "i") for h in leitor.fieldnames]
        dados = [linha for linha in leitor]
    print(f"📊 Registros carregados: {len(dados)}")
    print(f"🧩 Cabeçalhos detectados: {leitor.fieldnames}")
    return dados


def main():
    print("🚀 Iniciando análise de performance...\n")

    # Define pasta local e URLs de dados (2023 e 2024)
    pasta = os.getcwd()
    urls = [
        "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/EstadosBr_sat_ref/RJ/focos_br_rj_ref_2024.zip",
        "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/EstadosBr_sat_ref/RJ/focos_br_rj_ref_2023.zip"
    ]

    # Armazena todos os dados baixados
    todos_dados = []
    for url in urls:
        caminho_csv = baixar_e_extrair_csv(url, pasta)
        dados = carregar_dados(caminho_csv)
        todos_dados.extend(dados)

    print(f"\n📊 Total de registros carregados: {len(todos_dados)}\n")

    # Campos pelos quais será feita a ordenação
    criterios = ["data_pas", "bioma", "municipio"]

    resultados = []  # Armazena resultados de cada execução

    for criterio in criterios:
        print(f"🔽 Ordenando por: {criterio}")

        # --- Bubble Sort ---
        try:
            ordenado_bubble, comp_bubble, tempo_bubble = bubble_sort(todos_dados.copy(), criterio)
            print(f"✅ Bubble Sort concluído ({comp_bubble} comparações, {tempo_bubble:.4f}s)")
            resultados.append({
                "Criterio": criterio,
                "Algoritmo": "Bubble Sort",
                "Comparacoes": comp_bubble,
                "Tempo (s)": round(tempo_bubble, 6)
            })
        except KeyError as e:
            print(f"⚠️ Erro no Bubble Sort ({criterio}): {e}")
            continue

        # --- Quick Sort ---
        try:
            ordenado_quick, comp_quick, tempo_quick = quick_sort(todos_dados.copy(), criterio)
            print(f"✅ Quick Sort concluído ({comp_quick} comparações, {tempo_quick:.4f}s)\n")
            resultados.append({
                "Criterio": criterio,
                "Algoritmo": "Quick Sort",
                "Comparacoes": comp_quick,
                "Tempo (s)": round(tempo_quick, 6)
            })
        except Exception as e:
            print(f"⚠️ Erro no Quick Sort ({criterio}): {e}\n")

    # -----------------------------------------------------
    # 🧾 Gera o arquivo CSV final com os resultados obtidos
    # -----------------------------------------------------
    if resultados:
        nome_arquivo = os.path.join(pasta, "resultados.csv")
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            campos = ["Criterio", "Algoritmo", "Comparacoes", "Tempo (s)"]
            writer = csv.DictWriter(arquivo_csv, fieldnames=campos)
            writer.writeheader()
            writer.writerows(resultados)
        print(f"\n✅ Resultados salvos em '{nome_arquivo}'")
    else:
        print("⚠️ Nenhum resultado gerado.")


if __name__ == "__main__":
    main()