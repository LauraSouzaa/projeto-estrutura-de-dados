def busca_binaria(lista, valor, chave=lambda x: x):
    inicio = 0
    fim = len(lista) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        valor_meio = chave(lista[meio])

        if valor_meio == valor:
            return meio
        elif valor_meio < valor:
            inicio = meio + 1
        else:
            fim = meio - 1

    return -1
