# Projeto Sistema de Estoque e Vendas

## Disciplina

**Organização e Abstração na Programação**

## Trabalho

**Sistema de Estoque e Vendas**

## Integrantes

* Ana Luisa Rover de Moura
* João Pedro Lantelme
* Laura Portella de Souza
* Mateus Vicente Tortelli
* Wesley de Freitas

## Descrição do Sistema

Sistema desenvolvido em Python para gerenciamento de clientes, produtos, estoque e vendas, utilizando estruturas de dados e algoritmos de busca e ordenação.

O sistema permite cadastrar, consultar, alterar e remover clientes e produtos, controlar o estoque, registrar vendas, realizar buscas e desfazer a última operação realizada.

## Execução

É necessário ter o **Python 3** instalado.

1. Baixe ou clone o projeto.
2. Abra a pasta do projeto no terminal.
3. Execute:

```bash
python main.py
```

Os dados são carregados e salvos automaticamente nos arquivos CSV da pasta `data/`.

## Estrutura de Diretórios

```text
projeto-estrutura-de-dados/
├── main.py
├── algoritmos/
│   ├── busca_binaria.py
│   └── ordenacao.py
├── estruturas/
│   ├── fila.py
│   ├── lde.py
│   ├── lse.py
│   ├── nodo.py
│   └── pilha.py
├── models/
├── services/
└── data/
    ├── clientes.csv
    ├── produtos.csv
    └── vendas.csv
```

* **algoritmos:** algoritmos de ordenação e busca.
* **estruturas:** implementação das estruturas de dados.
* **models:** classes de Cliente, Produto e Venda.
* **services:** gerenciamento da persistência.
* **data:** arquivos CSV utilizados pelo sistema.

## Estruturas de Dados

### LSE — Lista Simplesmente Encadeada

Utilizada para armazenar os **clientes**. Cada elemento possui uma referência para o próximo elemento.

### LDE — Lista Duplamente Encadeada

Utilizada para armazenar os **produtos**. Cada elemento possui referências para o elemento anterior e o próximo.

### Fila

Utilizada para armazenar as **vendas**, seguindo o princípio **FIFO (First In, First Out)**, onde o primeiro elemento inserido é o primeiro a sair.

### Pilha

Utilizada para armazenar o **histórico de operações** e permitir a função de desfazer, seguindo o princípio **LIFO (Last In, First Out)**, onde a última operação inserida é a primeira a ser removida.

## Ordenação, Busca Binária e Persistência

### Algoritmo de Ordenação

O sistema utiliza o **Insertion Sort** para ordenar os produtos pelo ID.

### Busca Binária

A **Busca Binária** é utilizada para localizar produtos pelo ID. Para funcionar corretamente, os produtos precisam estar previamente ordenados.

### Persistência

Os dados do sistema são armazenados em arquivos **CSV**, permitindo que clientes, produtos e vendas sejam mantidos mesmo após o encerramento do programa.

Os principais arquivos são:

* `clientes.csv`
* `produtos.csv`
* `vendas.csv`

## Complexidade

| Algoritmo      | Melhor caso | Caso médio | Pior caso |
| -------------- | ----------- | ---------- | --------- |
| Insertion Sort | O(n)        | O(n²)      | O(n²)     |
| Busca Binária  | O(1)        | O(log n)   | O(log n)  |
