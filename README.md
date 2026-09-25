# Trabalho_ufu.1
# Inventário de Segurança — Ativos de TI e Vulnerabilidades

Trabalho de Cibersegurança (UFU), sprints 1 e 2, 2026/2.

Programa em Python, executado no terminal, que funciona como um pequeno
inventário de segurança: cadastra ativos de TI (servidores, notebooks,
roteadores etc.), registra as vulnerabilidades de cada um e permite
acompanhar o tratamento delas (aberta, em tratamento, corrigida ou aceita
como risco).

## Como executar

Só é preciso ter o Python 3.8 ou mais novo. Não há bibliotecas externas —
veja `requirements.txt`.

```bash
python3 main.py
```

Todos os arquivos `.py` precisam ficar na mesma pasta. Na primeira gravação o
programa cria o arquivo `ativos_db.txt`, que é a base de dados.

No VS Code: abra a **pasta** do projeto (não só o `main.py`) e aperte F5. A
pasta `.vscode/` já tem uma configuração que roda o programa no terminal
integrado, o que é necessário porque o programa usa `input()`.

## Menu

```
1  - Cadastrar novo ativo
2  - Consultar ativo (por ID, hostname exato ou trecho do hostname)
3  - Atualizar ativo
4  - Remover ativo
5  - Cadastrar vulnerabilidade em ativo existente
6  - Visualizar vulnerabilidades de um ativo
7  - Listar todos os ativos (ordenado por ID)
8  - Atualizar vulnerabilidade (ex.: mudar status)
9  - Remover vulnerabilidade
10 - Exportar relatório de vulnerabilidades (CSV)
0  - Sair
```

## Organização dos arquivos

| Arquivo | O que tem |
|---|---|
| `tipos.py` | Os `Enum`: `TipoAtivo`, `Severidade` e `StatusVulnerabilidade`, com os textos de exibição |
| `modelos.py` | As classes `Ativo` e `Vulnerabilidade` (dataclasses) |
| `banco_dados.py` | Leitura e gravação do arquivo e os dicionários de busca |
| `cores.py` | Cores ANSI para deixar severidade e status mais fáceis de ler no terminal |
| `main.py` | Menu, leitura dos dados digitados e as operações do CRUD |
| `test_banco_dados.py` | Testes automatizados da camada de persistência (`unittest`) |

## Requisitos da Tabela 1

| Req. | Onde está |
|---|---|
| 1 — Menu e tratamento de erros | `main.py`: `ler_inteiro`, `ler_texto`, `ler_sim_nao`, `escolher_enum`, `ler_numero_da_lista` e os `try/except` do `main()` |
| 2 — Enum com código inteiro | `tipos.py`: `TipoAtivo` (8 tipos, códigos de 1 a 8) |
| 3 — Cadastro gravado em arquivo | `banco_dados.py`: `salvar()` e `_carregar()`; arquivo `ativos_db.txt` |
| 4 — Busca por ID ou hostname | `main.py`: `buscar_ativo_interativo`; `banco_dados.py`: `buscar_por_id`, `buscar_por_hostname` e `buscar_por_trecho_hostname` |
| 5 — Atualizar ativo | `main.py`: `atualizar_ativo` |
| 6 — Remover ativo e suas vulnerabilidades | `main.py`: `deletar_ativo`; `banco_dados.py`: `remover` |
| 7 — Cadastrar vulnerabilidade a qualquer momento | `main.py`: `cadastrar_vulnerabilidade` |
| 8 — Visualizar vulnerabilidades | `main.py`: `visualizar_vulnerabilidades` |
| 9 — Dicionário | `banco_dados.py`: `ativos_por_id` e `ativos_por_hostname` |
| 10 — Git com branches e merge | Histórico do repositório (ver seção "Git" abaixo) |

Além dos requisitos, o programa tem funcionalidades extras (detalhadas mais
abaixo): editar e remover vulnerabilidades (opções 8 e 9), busca por trecho
do hostname, listagem ordenada, exportação de relatório em CSV e cores no
terminal.

## Por que um Enum plano com 8 tipos, e não uma estrutura de categorias

Uma versão inicial de estudo deste projeto (feita antes do `main.py` atual)
organizava os tipos de ativo em dois níveis: primeiro uma categoria
("Hardware", "Software", "Nuvem"...) e, dentro de cada categoria, um
dicionário de tipos. Essa estrutura também atende ao requisito 2, mas o
projeto final usa um único `Enum` plano (`TipoAtivo`, em `tipos.py`) com os
8 tipos lado a lado, sem agrupamento por categoria. A troca foi deliberada,
por três motivos:

1. **Validação de graça.** Um `Enum` garante, pela própria linguagem, que só
   existem os valores que foram declarados: não tem como criar um
   `TipoAtivo` com um código que não exista. Com dois níveis de `dict`, essa
   garantia teria que ser escrita à mão (validar a categoria e, dentro dela,
   o tipo).
2. **Leitura e gravação mais simples.** O ativo grava o `Enum` pelo nome
   (`self.tipo.name`, ex.: `"SERVIDOR"`) e volta a ser um objeto Python com
   `TipoAtivo[nome]`. Com dois níveis, seria preciso gravar e reconstruir
   duas informações (categoria e tipo) para cada ativo, e cuidar da
   consistência entre elas se um dia o mapeamento mudasse.
3. **O requisito pede "pelo menos 4 categorias com código", não
   necessariamente uma hierarquia.** Ler "categoria" como "os tipos de ativo
   reconhecidos pelo sistema" (que são pelo menos 4, na verdade são 8) é uma
   leitura válida do texto, e evita complexidade que o restante do programa
   não precisa: nenhuma operação do CRUD depende de agrupar os tipos por
   categoria.

Em compensação, a estrutura de dois níveis deixaria mais fácil, no futuro,
adicionar uma tela de "listar tipos por categoria" ou limitar quais tipos
fazem sentido para um determinado setor. Como isso não é pedido pela
Tabela 1, optei pela solução mais simples.

## Funcionalidades além da Tabela 1

**Busca por trecho do hostname (opção 2, item 3).** Além da busca exata
(que usa o dicionário `ativos_por_hostname` e satisfaz o requisito 9), o
menu de consulta agora aceita um pedaço do nome, útil quando o usuário não
lembra o hostname completo. Essa busca percorre os ativos um a um — é
propositalmente mais lenta que a busca exata, porque não faz sentido indexar
por "qualquer trecho possível de um texto" em um dicionário.

**Listagem ordenada por ID (opção 7).** Antes, a listagem seguia a ordem de
inserção no dicionário, que muda conforme ativos são cadastrados e
removidos. Agora ela é ordenada por ID antes de ser exibida.

**Editar e remover vulnerabilidades (opções 8 e 9).** Permitem, por exemplo,
mudar o status de uma vulnerabilidade de "Aberta" para "Corrigida" sem
precisar excluir e recadastrar, ou remover uma vulnerabilidade que não se
aplica mais. As vulnerabilidades aparecem numeradas na tela para facilitar a
escolha.

**Relatório de vulnerabilidades em CSV (opção 10).** Gera um arquivo `.csv`
com todas as vulnerabilidades de todos os ativos, ordenadas da mais grave
para a menos grave (Crítica → Alta → Média → Baixa). As colunas são
`severidade, id_ativo, hostname, categoria, descricao, status`. Se nenhum
nome de arquivo for digitado, usa `relatorio_vulnerabilidades.csv`.

**Cores no terminal (`cores.py`).** A severidade e o status de cada
vulnerabilidade aparecem coloridos (por exemplo, "Crítica" em vermelho,
"Corrigida" em verde), usando só códigos de escape ANSI — sem nenhuma
biblioteca externa como `colorama`. As cores são desligadas automaticamente
quando a saída não é um terminal (por exemplo, ao redirecionar para um
arquivo) ou quando a variável de ambiente `NO_COLOR` está definida. Em
terminais Windows muito antigos que não suportam ANSI, o texto pode aparecer
com os códigos de escape visíveis; nesse caso, defina `NO_COLOR=1` antes de
rodar o programa.

## Testes automatizados

`test_banco_dados.py` cobre a camada de persistência com `unittest` (só
biblioteca padrão, não precisa instalar `pytest`):

- cadastro e busca por ID e por hostname;
- recusa de ID e de hostname duplicados;
- remoção limpando os dois índices;
- persistência entre execuções (fechar e abrir a base de novo);
- reindexação depois de editar o hostname;
- busca por trecho do hostname;
- arquivo corrompido gerando backup em vez de perder dados;
- gravação atômica (sem sobrar arquivo `.tmp`).

Para rodar:

```bash
python -m unittest test_banco_dados.py -v
```

## Decisões de projeto

**Dois dicionários.** Os ativos ficam na memória em `ativos_por_id` (chave: o
número do ativo) e em `ativos_por_hostname` (chave: o hostname em minúsculas).
Assim a busca exata é direta pela chave, sem percorrer uma lista. Os dois
dicionários apontam para o mesmo objeto `Ativo`.

**Hostname único.** Como o hostname é chave de um dicionário, dois ativos com o
mesmo nome (ignorando maiúsculas e minúsculas) fariam um sobrescrever o outro
no índice. Por isso o cadastro e a atualização recusam hostnames repetidos.
`BancoDeDados.adicionar` também confere ID e hostname, para a base nunca ficar
inconsistente mesmo que o menu falhe em validar.

**Enum gravado pelo nome.** No arquivo, o tipo é gravado como `"SERVIDOR"` e
não como `2`. O arquivo fica legível e não depende da ordem dos números (ver
também a seção sobre o Enum plano, acima).

**Vulnerabilidades dentro do ativo.** Cada `Ativo` guarda a sua lista de
`Vulnerabilidade`. Por isso, remover o ativo remove as vulnerabilidades junto,
sem etapa extra.

**Formato do arquivo.** A base é JSON dentro de um `.txt`. É texto puro,
fácil de abrir e conferir, e o módulo `json` da biblioteca padrão faz a
conversão.

### Cuidados com o arquivo de dados

- **Base ilegível não é apagada.** Se o `ativos_db.txt` estiver corrompido ou
  com dados inválidos (JSON quebrado, tipo que não existe, ID ou hostname
  repetido), o programa renomeia o arquivo para
  `ativos_db.txt.AAAAMMDD_HHMMSS.bak`, avisa na tela e começa com uma base
  vazia. Se nem o backup puder ser criado, as gravações ficam bloqueadas
  naquela execução, para o arquivo original não ser sobrescrito.
- **Gravação em duas etapas.** O programa grava primeiro em `ativos_db.txt.tmp`
  e depois troca pelo arquivo definitivo. Se algo falhar durante a gravação, a
  base anterior continua intacta.

### Tratamento de erros e interrupção

- Números inválidos, campos vazios e opções fora da lista são pedidos de novo.
- **Ctrl+C no menu** encerra o programa. **Ctrl+C durante uma operação** cancela
  só a operação e volta ao menu. Nas atualizações, o ativo (ou a
  vulnerabilidade) só é alterado depois de todas as respostas serem lidas,
  então cancelar no meio não deixa nada pela metade.
- **Ctrl+D** (fim da entrada) encerra o programa sem mostrar erro.
- Qualquer outra falha inesperada em uma operação é mostrada como mensagem e o
  programa volta ao menu.

## Git

O repositório tem mais de duas branches (`main` e mais duas de funcionalidade)
e os merges foram feitos com `--no-ff`, para o merge aparecer como um commit
próprio no histórico:

```bash
git init
git add .
git commit -m "Estrutura inicial: enums e modelos"

git checkout -b feature/cadastro-ativos
# ... commits do CRUD de ativos ...
git checkout main
git merge --no-ff feature/cadastro-ativos

git checkout -b feature/vulnerabilidades
# ... commits do CRUD de vulnerabilidades ...
git checkout main
git merge --no-ff feature/vulnerabilidades

git remote add origin <url-do-repositorio>
git push -u origin --all
```

O `.gitignore` já está pronto na raiz do projeto e cobre os arquivos gerados
pela execução (base de dados, relatórios CSV, `__pycache__`), que não fazem
parte do código-fonte.
