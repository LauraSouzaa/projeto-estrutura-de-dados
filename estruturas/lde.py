from estruturas.nodo import Nodo


class LDE:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def esta_vazia(self):
        return self.inicio is None

    def inserir(self, dado):
        novo = Nodo(dado)

        if self.inicio is None:
            self.inicio = self.fim = novo
        else:
            novo.anterior = self.fim
            self.fim.proximo = novo
            self.fim = novo

        self.tamanho += 1

    def buscar(self, id):
        atual = self.inicio
        while atual:
            if atual.dado.id == id:
                return atual.dado
            atual = atual.proximo
        return None

    def remover(self, id):
        atual = self.inicio

        while atual:
            if atual.dado.id == id:
                if atual.anterior:
                    atual.anterior.proximo = atual.proximo
                else:
                    self.inicio = atual.proximo

                if atual.proximo:
                    atual.proximo.anterior = atual.anterior
                else:
                    self.fim = atual.anterior

                self.tamanho -= 1
                return atual.dado

            atual = atual.proximo

        return None

    def para_lista(self):
        resultado = []
        atual = self.inicio
        while atual:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado

    def para_lista_inversa(self):
        resultado = []
        atual = self.fim
        while atual:
            resultado.append(atual.dado)
            atual = atual.anterior
        return resultado
