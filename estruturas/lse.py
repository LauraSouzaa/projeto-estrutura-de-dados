from estruturas.nodo import Nodo


class LSE:
    def __init__(self):
        self.inicio = None
        self.tamanho = 0

    def esta_vazia(self):
        return self.inicio is None

    def inserir(self, dado):
        novo = Nodo(dado)
        if self.inicio is None:
            self.inicio = novo
        else:
            atual = self.inicio
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo
        self.tamanho += 1

    def buscar(self, id):
        atual = self.inicio
        while atual:
            if atual.dado.id == id:
                return atual.dado
            atual = atual.proximo
        return None

    def remover(self, id):
        anterior = None
        atual = self.inicio

        while atual:
            if atual.dado.id == id:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                self.tamanho -= 1
                return atual.dado
            anterior = atual
            atual = atual.proximo
        return None

    def para_lista(self):
        resultado = []
        atual = self.inicio
        while atual:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado
