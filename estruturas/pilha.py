from estruturas.nodo import Nodo


class Pilha:
    def __init__(self):
        self.topo = None
        self.tamanho = 0

    def esta_vazia(self):
        return self.topo is None

    def empilhar(self, dado):
        novo = Nodo(dado)
        novo.proximo = self.topo
        self.topo = novo
        self.tamanho += 1

    def desempilhar(self):
        if self.topo is None:
            return None
        dado = self.topo.dado
        self.topo = self.topo.proximo
        self.tamanho -= 1
        return dado

    def topo_item(self):
        return self.topo.dado if self.topo else None
