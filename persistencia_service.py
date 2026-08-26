import csv
import os

from cliente import Cliente
from produto import Produto
from venda import Venda


class PersistenciaService:
    def __init__(self, pasta):
        self.pasta = pasta
        os.makedirs(self.pasta, exist_ok=True)

        self.clientes_path = os.path.join(pasta, "clientes.csv")
        self.produtos_path = os.path.join(pasta, "produtos.csv")
        self.vendas_path = os.path.join(pasta, "vendas.csv")

    def salvar_clientes(self, clientes):
        with open(self.clientes_path, "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["id", "nome"])
            for cliente in clientes.para_lista():
                writer.writerow([cliente.id, cliente.nome])

    def salvar_produtos(self, produtos):
        with open(self.produtos_path, "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["id", "nome", "quantidade", "preco"])
            for produto in produtos.para_lista():
                writer.writerow([
                    produto.id, produto.nome, produto.quantidade, produto.preco
                ])

    def salvar_vendas(self, fila):
        with open(self.vendas_path, "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["id", "cliente_id", "itens", "total"])

            for venda in fila.para_lista():
                itens = ";".join(
                    f"{produto_id}:{quantidade}"
                    for produto_id, quantidade in venda.itens
                )
                writer.writerow([venda.id, venda.cliente_id, itens, venda.total])

    def carregar_clientes(self, clientes):
        if not os.path.exists(self.clientes_path):
            return

        try:
            with open(self.clientes_path, newline="", encoding="utf-8") as arquivo:
                reader = csv.DictReader(arquivo)
                for linha in reader:
                    if not linha.get("id") or not linha.get("nome"):
                        continue
                    try:
                        cliente = Cliente(int(linha["id"]), linha["nome"].strip())
                        if not clientes.buscar(cliente.id):
                            clientes.inserir(cliente)
                    except (ValueError, TypeError):
                        continue
        except (OSError, csv.Error):
            print("Aviso: não foi possível carregar clientes.csv.")

    def carregar_produtos(self, produtos):
        if not os.path.exists(self.produtos_path):
            return

        try:
            with open(self.produtos_path, newline="", encoding="utf-8") as arquivo:
                reader = csv.DictReader(arquivo)
                for linha in reader:
                    try:
                        produto = Produto(
                            int(linha["id"]),
                            linha["nome"].strip(),
                            int(linha["quantidade"]),
                            float(linha["preco"])
                        )
                        if not produtos.buscar(produto.id):
                            produtos.inserir(produto)
                    except (ValueError, TypeError, KeyError):
                        continue
        except (OSError, csv.Error):
            print("Aviso: não foi possível carregar produtos.csv.")

    def carregar_vendas(self, fila, clientes, produtos):
        if not os.path.exists(self.vendas_path):
            return

        try:
            with open(self.vendas_path, newline="", encoding="utf-8") as arquivo:
                reader = csv.DictReader(arquivo)

                for linha in reader:
                    try:
                        venda_id = int(linha["id"])
                        cliente_id = int(linha["cliente_id"])

                        if not clientes.buscar(cliente_id):
                            continue

                        itens = []
                        texto_itens = linha.get("itens", "").strip()

                        if texto_itens:
                            for item in texto_itens.split(";"):
                                produto_id, quantidade = item.split(":")
                                produto_id = int(produto_id)
                                quantidade = int(quantidade)

                                if produtos.buscar(produto_id):
                                    itens.append((produto_id, quantidade))

                        if itens:
                            venda = Venda(venda_id, cliente_id, itens, produtos)
                            fila.enfileirar(venda)

                    except (ValueError, TypeError, KeyError):
                        continue

        except (OSError, csv.Error):
            print("Aviso: não foi possível carregar vendas.csv.")
