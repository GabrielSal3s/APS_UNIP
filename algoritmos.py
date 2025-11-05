import time
import csv

def normalizar(valor):
    """Remove espaços e converte o valor para minúsculas para comparação."""
    return str(valor).strip().lower()

def bubble_sort(dados, chave):
    """Ordena uma lista de dicionários pelo campo 'chave' usando Bubble Sort."""
    inicio = time.time()
    n = len(dados)
    comparacoes = 0

    for i in range(n - 1):
        for j in range(n - 1 - i):
            comparacoes += 1
            if normalizar(dados[j][chave]) > normalizar(dados[j + 1][chave]):
                dados[j], dados[j + 1] = dados[j + 1], dados[j]

    tempo = time.time() - inicio
    return dados, comparacoes, tempo

def quick_sort(dados, chave):
    """Ordena uma lista de dicionários pelo campo 'chave' usando Quick Sort."""
    inicio = time.time()
    comparacoes = [0]

    def _quick_sort(lista):
        if len(lista) <= 1:
            return lista
        pivo = lista[len(lista) // 2]
        menores, iguais, maiores = [], [], []
        for item in lista:
            comparacoes[0] += 1
            if normalizar(item[chave]) < normalizar(pivo[chave]):
                menores.append(item)
            elif normalizar(item[chave]) > normalizar(pivo[chave]):
                maiores.append(item)
            else:
                iguais.append(item)
        return _quick_sort(menores) + iguais + _quick_sort(maiores)

    try:
        resultado = _quick_sort(dados)
    except RecursionError:
        resultado = sorted(dados, key=lambda x: normalizar(x[chave]))
    tempo = time.time() - inicio
    return resultado, comparacoes[0], tempo

# -------------------------------------------------------------------
# 🚀 Execução principal e geração da planilha de resultados
# -------------------------------------------------------------------

if __name__ == "__main__":
    # Exemplo de dados simulados (substitua depois pelos reais)
    dados_exemplo = [
        {"municipio": "São Paulo", "valor": 300},
        {"municipio": "Campinas", "valor": 150},
        {"municipio": "Santos", "valor": 210},
        {"municipio": "Sorocaba", "valor": 180},
    ]

    # Escolher a chave de ordenação
    chave = "municipio"

    # Executar os dois algoritmos
    bubble_ordenado, bubble_comp, bubble_tempo = bubble_sort(dados_exemplo.copy(), chave)
    quick_ordenado, quick_comp, quick_tempo = quick_sort(dados_exemplo.copy(), chave)

    # Criar lista consolidada de resultados
    resultados = [
        {"Algoritmo": "Bubble Sort", "Comparações": bubble_comp, "Tempo (s)": round(bubble_tempo, 6)},
        {"Algoritmo": "Quick Sort", "Comparações": quick_comp, "Tempo (s)": round(quick_tempo, 6)},
    ]

    # Escrever planilha CSV
    with open("resultados.csv", mode="w", newline="", encoding="utf-8") as arquivo_csv:
        campos = ["Algoritmo", "Comparações", "Tempo (s)"]
        writer = csv.DictWriter(arquivo_csv, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resultados)

    print("✅ Resultados salvos em 'resultados.csv'")
    print("📊 Comparação de desempenho:")
    for r in resultados:
        print(r)