class Produto:
    def __init__(self, id, nome, quantidade, preco):
        if preco <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")

        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return (
            f"ID: {self.id} | Nome: {self.nome} | "
            f"Estoque: {self.quantidade} | Preço: R$ {self.preco:.2f}"
        )
