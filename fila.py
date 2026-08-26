from nodo import Nodo


class Fila:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def esta_vazia(self):
        return self.inicio is None

    def enfileirar(self, dado):
        novo = Nodo(dado)
        if self.fim is None:
            self.inicio = self.fim = novo
        else:
            self.fim.proximo = novo
            self.fim = novo
        self.tamanho += 1

    def desenfileirar(self):
        if self.inicio is None:
            return None
        dado = self.inicio.dado
        self.inicio = self.inicio.proximo
        if self.inicio is None:
            self.fim = None
        self.tamanho -= 1
        return dado

    def primeiro(self):
        return self.inicio.dado if self.inicio else None

    def para_lista(self):
        resultado = []
        atual = self.inicio
        while atual:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado

    def proximo_id(self):
        maior = 0
        for venda in self.para_lista():
            if venda.id > maior:
                maior = venda.id
        return maior + 1

    def valor_total(self):
        return sum(venda.total for venda in self.para_lista())

    def cliente_tem_venda(self, cliente_id):
        return any(v.cliente_id == cliente_id for v in self.para_lista())

    def produto_tem_venda(self, produto_id):
        return any(
            any(pid == produto_id for pid, _ in venda.itens)
            for venda in self.para_lista()
        )

    def remover_por_id(self, venda_id):
        anterior = None
        atual = self.inicio

        while atual:
            if atual.dado.id == venda_id:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo

                if atual == self.fim:
                    self.fim = anterior

                self.tamanho -= 1
                return atual.dado

            anterior = atual
            atual = atual.proximo

        return None
