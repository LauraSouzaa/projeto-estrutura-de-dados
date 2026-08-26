from models.cliente import Cliente
from models.produto import Produto
from models.venda import Venda
from estruturas.lse import LSE
from estruturas.lde import LDE
from estruturas.fila import Fila
from estruturas.pilha import Pilha
from algoritmos.ordenacao import insertion_sort
from algoritmos.busca_binaria import busca_binaria
from services.persistencia_service import PersistenciaService

DATA_DIR = "data"

clientes = LSE()
produtos = LDE()
fila_vendas = Fila()
pilha_historico = Pilha()
persistencia = PersistenciaService(DATA_DIR)


def carregar_dados():
    persistencia.carregar_clientes(clientes)
    persistencia.carregar_produtos(produtos)
    persistencia.carregar_vendas(fila_vendas, clientes, produtos)


def salvar_dados():
    persistencia.salvar_clientes(clientes)
    persistencia.salvar_produtos(produtos)
    persistencia.salvar_vendas(fila_vendas)


def ler_int(msg, minimo=None):
    while True:
        try:
            valor = int(input(msg))
            if minimo is not None and valor < minimo:
                raise ValueError
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro válido.")


def ler_float(msg, minimo=None):
    while True:
        try:
            valor = float(input(msg).replace(",", "."))
            if minimo is not None and valor <= minimo:
                raise ValueError
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número válido.")


def ler_texto(msg):
    while True:
        valor = input(msg).strip()
        if valor:
            return valor
        print("O campo não pode ficar vazio.")


def encontrar_cliente(cliente_id):
    return clientes.buscar(cliente_id)


def encontrar_produto(produto_id):
    return produtos.buscar(produto_id)


def cadastrar_cliente():
    cliente_id = ler_int("ID do cliente: ", 1)
    if encontrar_cliente(cliente_id):
        print("Já existe um cliente com esse ID.")
        return

    nome = ler_texto("Nome: ")
    clientes.inserir(Cliente(cliente_id, nome))
    salvar_dados()
    pilha_historico.empilhar(("cadastrar_cliente", cliente_id))
    print("Cliente cadastrado com sucesso.")


def listar_clientes():
    itens = clientes.para_lista()
    if not itens:
        print("Nenhum cliente cadastrado.")
        return
    print("\n--- CLIENTES ---")
    for cliente in itens:
        print(cliente)


def buscar_cliente():
    cliente_id = ler_int("ID do cliente: ", 1)
    cliente = encontrar_cliente(cliente_id)
    print(cliente if cliente else "Cliente não encontrado.")


def remover_cliente():
    cliente_id = ler_int("ID do cliente: ", 1)
    cliente = encontrar_cliente(cliente_id)

    if not cliente:
        print("Cliente não encontrado.")
        return

    clientes.remover(cliente_id)
    salvar_dados()
    pilha_historico.empilhar(("remover_cliente", cliente))

    print("Cliente removido com sucesso.")


def cadastrar_produto():
    produto_id = ler_int("ID do produto: ", 1)
    if encontrar_produto(produto_id):
        print("Já existe um produto com esse ID.")
        return

    nome = ler_texto("Nome: ")
    quantidade = ler_int("Quantidade inicial: ", 0)
    preco = ler_float("Preço: ", 0)

    produtos.inserir(Produto(produto_id, nome, quantidade, preco))
    salvar_dados()
    pilha_historico.empilhar(("cadastrar_produto", produto_id))
    print("Produto cadastrado com sucesso.")


def listar_produtos():
    itens = produtos.para_lista()
    if not itens:
        print("Nenhum produto cadastrado.")
        return
    print("\n--- PRODUTOS ---")
    for produto in itens:
        print(produto)


def buscar_produto():
    produto_id = ler_int("ID do produto: ", 1)
    produto = encontrar_produto(produto_id)
    print(produto if produto else "Produto não encontrado.")


def atualizar_estoque():
    produto_id = ler_int("ID do produto: ", 1)
    produto = encontrar_produto(produto_id)
    if not produto:
        print("Produto não encontrado.")
        return

    nova_quantidade = ler_int("Nova quantidade: ", 0)
    quantidade_anterior = produto.quantidade
    produto.quantidade = nova_quantidade
    salvar_dados()
    pilha_historico.empilhar(("atualizar_estoque", produto_id, quantidade_anterior))
    print("Estoque atualizado.")


def remover_produto():
    produto_id = ler_int("ID do produto: ", 1)
    produto = encontrar_produto(produto_id)
    if not produto:
        print("Produto não encontrado.")
        return

    if fila_vendas.produto_tem_venda(produto_id):
        print("Não é possível remover um produto que possui vendas registradas.")
        return

    produtos.remover(produto_id)
    salvar_dados()
    pilha_historico.empilhar(("remover_produto", produto))
    print("Produto removido com sucesso.")


def produtos_inversos():
    itens = produtos.para_lista_inversa()
    if not itens:
        print("Nenhum produto cadastrado.")
        return
    for produto in itens:
        print(produto)


def produtos_ordenados():
    itens = produtos.para_lista()
    if not itens:
        print("Nenhum produto cadastrado.")
        return
    ordenados = insertion_sort(itens, chave=lambda p: p.id)
    print("\n--- PRODUTOS ORDENADOS POR ID ---")
    for produto in ordenados:
        print(produto)


def buscar_binaria_produto():
    itens = produtos.para_lista()
    if not itens:
        print("Nenhum produto cadastrado.")
        return

    ordenados = insertion_sort(itens, chave=lambda p: p.id)
    produto_id = ler_int("ID do produto: ", 1)
    indice = busca_binaria(ordenados, produto_id, chave=lambda p: p.id)

    if indice == -1:
        print("Produto não encontrado.")
    else:
        print("Produto encontrado:")
        print(ordenados[indice])


def realizar_venda():
    if clientes.esta_vazia():
        print("Cadastre pelo menos um cliente antes de vender.")
        return
    if produtos.esta_vazia():
        print("Cadastre pelo menos um produto antes de vender.")
        return

    cliente_id = ler_int("ID do cliente: ", 1)
    cliente = encontrar_cliente(cliente_id)
    if not cliente:
        print("Cliente não encontrado. Venda cancelada.")
        return

    quantidade_itens = ler_int("Quantidade de produtos diferentes na venda: ", 1)
    itens = []

    for _ in range(quantidade_itens):
        produto_id = ler_int("ID do produto: ", 1)
        produto = encontrar_produto(produto_id)
        if not produto:
            print("Produto não encontrado. Venda cancelada.")
            return

        quantidade = ler_int("Quantidade: ", 1)

        # Evita repetir o mesmo produto na mesma venda.
        for item_id, _ in itens:
            if item_id == produto_id:
                print("O mesmo produto não pode ser informado duas vezes na venda.")
                return

        if produto.quantidade < quantidade:
            print(f"Estoque insuficiente para {produto.nome}. Disponível: {produto.quantidade}.")
            return

        itens.append((produto_id, quantidade))

    venda_id = fila_vendas.proximo_id()
    venda = Venda(venda_id, cliente_id, itens, produtos)

    # Só altera estoque depois de todas as validações.
    for produto_id, quantidade in itens:
        produto = encontrar_produto(produto_id)
        produto.quantidade -= quantidade

    fila_vendas.enfileirar(venda)
    pilha_historico.empilhar(("venda", venda))
    salvar_dados()
    print(f"Venda #{venda.id} realizada com sucesso. Total: R$ {venda.total:.2f}")


def visualizar_fila():
    if fila_vendas.esta_vazia():
        print("A fila de vendas está vazia.")
        return
    print("\n--- FILA DE VENDAS (FIFO) ---")
    for venda in fila_vendas.para_lista():
        print(venda)


def visualizar_primeira_venda():
    venda = fila_vendas.primeiro()
    print(venda if venda else "A fila de vendas está vazia.")


def valor_total_estoque():
    total = sum(p.quantidade * p.preco for p in produtos.para_lista())
    print(f"Valor total do estoque: R$ {total:.2f}")


def valor_total_vendas():
    total = fila_vendas.valor_total()
    print(f"Valor total das vendas: R$ {total:.2f}")


def clientes_gastos():
    vendas = fila_vendas.para_lista()
    if not vendas:
        print("Nenhuma venda registrada.")
        return

    gastos = {}
    for venda in vendas:
        gastos[venda.cliente_id] = gastos.get(venda.cliente_id, 0) + venda.total

    print("\n--- CLIENTES E VALORES GASTOS ---")
    for cliente in clientes.para_lista():
        print(f"{cliente.nome}: R$ {gastos.get(cliente.id, 0):.2f}")


def cliente_que_mais_gastou():
    vendas = fila_vendas.para_lista()
    if not vendas:
        print("Nenhuma venda registrada.")
        return

    gastos = {}
    for venda in vendas:
        gastos[venda.cliente_id] = gastos.get(venda.cliente_id, 0) + venda.total

    cliente_id = max(gastos, key=gastos.get)
    cliente = encontrar_cliente(cliente_id)
    print(f"Cliente que mais gastou: {cliente.nome} - R$ {gastos[cliente_id]:.2f}")


def produto_mais_vendido():
    vendas = fila_vendas.para_lista()
    if not vendas:
        print("Nenhuma venda registrada.")
        return

    quantidades = {}
    for venda in vendas:
        for produto_id, quantidade in venda.itens:
            quantidades[produto_id] = quantidades.get(produto_id, 0) + quantidade

    produto_id = max(quantidades, key=quantidades.get)
    produto = encontrar_produto(produto_id)
    print(f"Produto mais vendido: {produto.nome} - {quantidades[produto_id]} unidade(s)")


def desfazer():
    if pilha_historico.esta_vazia():
        print("Não há operações para desfazer.")
        return

    operacao = pilha_historico.desempilhar()
    tipo = operacao[0]

    if tipo == "venda":
        venda = operacao[1]
        if fila_vendas.remover_por_id(venda.id):
            for produto_id, quantidade in venda.itens:
                produto = encontrar_produto(produto_id)
                if produto:
                    produto.quantidade += quantidade
            salvar_dados()
            print(f"Venda #{venda.id} desfeita. Estoque restaurado.")

    elif tipo == "cadastrar_cliente":
        clientes.remover(operacao[1])
        salvar_dados()
        print("Cadastro do cliente desfeito.")

    elif tipo == "remover_cliente":
        clientes.inserir(operacao[1])
        salvar_dados()
        print("Remoção do cliente desfeita.")

    elif tipo == "cadastrar_produto":
        produtos.remover(operacao[1])
        salvar_dados()
        print("Cadastro do produto desfeito.")

    elif tipo == "remover_produto":
        produtos.inserir(operacao[1])
        salvar_dados()
        print("Remoção do produto desfeita.")

    elif tipo == "atualizar_estoque":
        produto = encontrar_produto(operacao[1])
        if produto:
            produto.quantidade = operacao[2]
            salvar_dados()
            print("Atualização de estoque desfeita.")
        else:
            print("Não foi possível desfazer: produto não existe mais.")


def menu():
    print("""
==============================
 SISTEMA DE ESTOQUE E VENDAS
==============================
1  - Cadastrar cliente
2  - Listar clientes
3  - Buscar cliente
4  - Remover cliente
5  - Cadastrar produto
6  - Listar produtos
7  - Buscar produto
8  - Atualizar estoque
9  - Remover produto
10 - Listar produtos em ordem inversa
11 - Listar produtos ordenados
12 - Buscar produto por ID usando Busca Binária
13 - Realizar venda
14 - Visualizar fila de vendas
15 - Visualizar primeira venda da fila
16 - Exibir valor total do estoque
17 - Exibir valor total das vendas
18 - Exibir clientes e valores totais gastos
19 - Exibir cliente que mais gastou
20 - Exibir produto mais vendido
21 - Desfazer última operação
0  - Sair
""")


def main():
    carregar_dados()
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            op = int(opcao)
        except ValueError:
            print("Opção inválida.")
            continue

        if op == 0:
            print("Programa encerrado.")
            break
        elif op == 1:
            cadastrar_cliente()
        elif op == 2:
            listar_clientes()
        elif op == 3:
            buscar_cliente()
        elif op == 4:
            remover_cliente()
        elif op == 5:
            cadastrar_produto()
        elif op == 6:
            listar_produtos()
        elif op == 7:
            buscar_produto()
        elif op == 8:
            atualizar_estoque()
        elif op == 9:
            remover_produto()
        elif op == 10:
            produtos_inversos()
        elif op == 11:
            produtos_ordenados()
        elif op == 12:
            buscar_binaria_produto()
        elif op == 13:
            realizar_venda()
        elif op == 14:
            visualizar_fila()
        elif op == 15:
            visualizar_primeira_venda()
        elif op == 16:
            valor_total_estoque()
        elif op == 17:
            valor_total_vendas()
        elif op == 18:
            clientes_gastos()
        elif op == 19:
            cliente_que_mais_gastou()
        elif op == 20:
            produto_mais_vendido()
        elif op == 21:
            desfazer()
        else:
            print("Opção inválida. Escolha uma opção do menu.")


if __name__ == "__main__":
    main()
