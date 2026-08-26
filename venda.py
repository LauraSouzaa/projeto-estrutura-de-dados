class Venda:
    def __init__(self, id, cliente_id, itens, produtos):
        self.id = id
        self.cliente_id = cliente_id
        self.itens = itens[:]  # [(produto_id, quantidade), ...]
        self.total = 0.0

        for produto_id, quantidade in self.itens:
            produto = produtos.buscar(produto_id)
            self.total += produto.preco * quantidade

    def __str__(self):
        itens = ", ".join(
            f"Produto {produto_id} x{quantidade}"
            for produto_id, quantidade in self.itens
        )
        return (
            f"Venda #{self.id} | Cliente: {self.cliente_id} | "
            f"{itens} | Total: R$ {self.total:.2f}"
        )