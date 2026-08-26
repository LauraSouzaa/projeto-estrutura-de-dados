def insertion_sort(lista, chave=lambda x: x):
    # Ordenação manual: não utiliza sort() nem sorted().
    resultado = lista[:]

    for i in range(1, len(resultado)):
        atual = resultado[i]
        j = i - 1

        while j >= 0 and chave(resultado[j]) > chave(atual):
            resultado[j + 1] = resultado[j]
            j -= 1

        resultado[j + 1] = atual

    return resultado
