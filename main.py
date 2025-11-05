from utils import baixar_e_extrair_zip, ler_coluna_frp
from algoritmos import bubble_sort, quick_sort
import csv
import os
import time

def salvar_resultados(resultados):
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta_atual, "resultados.csv")
    cabecalho = ["algoritimos", "comparacoes", "tempo_exec"]

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho)
        writer.writeheader()
        writer.writerows(resultados)
    print(f"✅ Resultados salvos em: {caminho}")

def main():
    print("🚀 Iniciando processo...")
    url_zip = "https://queimadas.dgi.inpe.br/queimadas/portal-static/estatisticas_estados/Estados_2025.zip"

    caminho_csv = baixar_e_extrair_zip(url_zip)
    if not caminho_csv:
        print("⚠️ Não foi possível obter o CSV.")
        return

    dados = ler_coluna_frp(caminho_csv)
    if not dados:
        print("⚠️ Nenhum dado disponível para ordenação.")
        return

    resultados = []

    # Bubble Sort
    inicio = time.time()
    _, comp_bubble = bubble_sort(dados.copy())
    tempo_bubble = time.time() - inicio
    resultados.append({
        "algoritimos": "Bubble Sort",
        "comparacoes": comp_bubble,
        "tempo_exec": round(tempo_bubble, 4)
    })

    # Quick Sort
    inicio = time.time()
    _, comp_quick = quick_sort(dados.copy())
    tempo_quick = time.time() - inicio
    resultados.append({
        "algoritimos": "Quick Sort",
        "comparacoes": comp_quick,
        "tempo_exec": round(tempo_quick, 4)
    })

    salvar_resultados(resultados)

if __name__ == "__main__":
    main()