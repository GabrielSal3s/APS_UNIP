def bubble_sort(lista):
    n = len(lista)
    comparacoes = 0
    for i in range(n):
        trocou = False
        for j in range(0, n - i - 1):
            comparacoes += 1
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        if not trocou:
            break
    return lista, comparacoes

def quick_sort(lista):
    comparacoes = [0]

    def _quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left, middle, right = [], [], []
        for x in arr:
            comparacoes[0] += 1
            if x < pivot:
                left.append(x)
            elif x > pivot:
                right.append(x)
            else:
                middle.append(x)
        return _quick_sort(left) + middle + _quick_sort(right)