"""
Sistema de Inventário de Segurança - Ativos de TI e Vulnerabilidades
Trabalho de Ciberseguranca - UFU (Sprints 1 e 2)

Execução: python main.py
"""

from __future__ import annotations  # garante compatibilidade com Python 3.8+

import csv
from typing import List, Optional, Tuple

from tipos import TipoAtivo, Severidade, StatusVulnerabilidade, rotulo_severidade, rotulo_status
from modelos import Ativo, Vulnerabilidade
from banco_dados import BancoDeDados


# ------------------------------------------------------------------
# Funções auxiliares de entrada de dados (Requisito 1: tratamento de erros)
# ------------------------------------------------------------------

def ler_inteiro(mensagem: str, minimo: Optional[int] = None) -> int:
    """Lê um inteiro do usuário, repetindo até obter uma entrada válida."""
    while True:
        valor = input(mensagem).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            continue
        if minimo is not None and numero < minimo:
            print(f"O valor deve ser maior ou igual a {minimo}.")
            continue
        return numero


def ler_texto(mensagem: str, permitir_vazio: bool = False) -> str:
    """Lê uma string não vazia (a menos que permitir_vazio=True)."""
    while True:
        valor = input(mensagem).strip()
        if valor or permitir_vazio:
            return valor
        print("Este campo não pode ficar vazio.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        valor = input(mensagem).strip().lower()
        if valor in ("s", "sim"):
            return True
        if valor in ("n", "nao", "não"):
            return False
        print("Responda apenas com 's' ou 'n'.")


def ler_numero_da_lista(mensagem: str, total: int) -> int:
    """Lê um número entre 1 e 'total' (posição de um item numa lista exibida)."""
    while True:
        numero = ler_inteiro(mensagem, minimo=1)
        if numero <= total:
            return numero
        print(f"Escolha um número entre 1 e {total}.")


def escolher_enum(mensagem: str, enum_classe):
    """Exibe as opções de um Enum e retorna o valor escolhido pelo usuário."""
    opcoes = list(enum_classe)
    print(mensagem)
    for opcao in opcoes:
        print(f"  {opcao.value} - {opcao.name}")
    while True:
        escolha = ler_inteiro("Escolha o código da opção: ")
        for opcao in opcoes:
            if opcao.value == escolha:
                return opcao
        print("Código inválido. Tente novamente.")


# ------------------------------------------------------------------
# Requisito 3: Cadastro de ativo (Create)
# ------------------------------------------------------------------

def cadastrar_ativo(db: BancoDeDados) -> None:
    print("\n--- Cadastro de novo ativo de TI ---")
    while True:
        id_ativo = ler_inteiro("ID único do ativo (número inteiro): ", minimo=1)
        if db.existe_id(id_ativo):
            print("Já existe um ativo com esse ID. Escolha outro.")
            continue
        break

    # O hostname também precisa ser único, pois é usado como chave de busca.
    while True:
        hostname = ler_texto("Nome/Hostname do ativo: ")
        if db.existe_hostname(hostname):
            print("Já existe um ativo com esse hostname. Escolha outro.")
            continue
        break

    responsavel = ler_texto("Responsável: ")
    setor = ler_texto("Setor/Localização: ")
    tipo = escolher_enum("Tipo de ativo:", TipoAtivo)

    vulnerabilidades = []
    if ler_sim_nao("Deseja cadastrar vulnerabilidades iniciais já conhecidas? (s/n): "):
        vulnerabilidades = ler_multiplas_vulnerabilidades()

    ativo = Ativo(id_ativo, hostname, responsavel, setor, tipo, vulnerabilidades)
    db.adicionar(ativo)
    print(f"\nAtivo '{hostname}' cadastrado com sucesso (ID {id_ativo}).")


def ler_multiplas_vulnerabilidades() -> List[Vulnerabilidade]:
    vulnerabilidades = []
    while True:
        descricao = ler_texto("  Descrição da vulnerabilidade: ")
        categoria = ler_texto(
            "  Categoria (ex.: senha fraca, software desatualizado, exposição de serviço): "
        )
        severidade = escolher_enum("  Severidade:", Severidade)
        status = escolher_enum("  Status de tratamento:", StatusVulnerabilidade)
        vulnerabilidades.append(Vulnerabilidade(descricao, categoria, severidade, status))
        if not ler_sim_nao("  Adicionar outra vulnerabilidade a este ativo? (s/n): "):
            break
    return vulnerabilidades


# ------------------------------------------------------------------
# Requisito 4: Consulta de ativo (Read)
# ------------------------------------------------------------------

def buscar_ativo_interativo(db: BancoDeDados) -> None:
    print("\n--- Consulta de ativo ---")
    print("1 - Buscar por ID")
    print("2 - Buscar por hostname (nome exato)")
    print("3 - Buscar por trecho do hostname")
    opcao = ler_inteiro("Escolha: ")

    if opcao == 1:
        id_ativo = ler_inteiro("ID do ativo: ")
        ativo = db.buscar_por_id(id_ativo)
        print("\n" + str(ativo) if ativo else "Ativo não encontrado.")
    elif opcao == 2:
        hostname = ler_texto("Hostname: ")
        ativo = db.buscar_por_hostname(hostname)
        print("\n" + str(ativo) if ativo else "Ativo não encontrado.")
    elif opcao == 3:
        trecho = ler_texto("Trecho do hostname: ")
        encontrados = sorted(
            db.buscar_por_trecho_hostname(trecho), key=lambda a: a.id_ativo
        )
        if not encontrados:
            print("Nenhum ativo encontrado com esse trecho no hostname.")
            return
        print(f"\n{len(encontrados)} ativo(s) encontrado(s):")
        for ativo in encontrados:
            print("\n" + str(ativo))
    else:
        print("Opção inválida.")


# ------------------------------------------------------------------
# Requisito 5: Atualização de ativo (Update)
# ------------------------------------------------------------------

def atualizar_ativo(db: BancoDeDados) -> None:
    print("\n--- Atualização de ativo ---")
    id_ativo = ler_inteiro("ID do ativo a atualizar: ")
    ativo = db.buscar_por_id(id_ativo)
    if not ativo:
        print("Ativo não encontrado.")
        return

    print("Pressione Enter sem digitar nada para manter o valor atual.")

    # Primeiro coleta todas as respostas; só no fim altera o ativo. Assim, se o
    # usuário cancelar no meio (Ctrl+C), nada fica alterado pela metade.
    while True:
        novo_hostname = ler_texto(f"Hostname [{ativo.hostname}]: ", permitir_vazio=True)
        if novo_hostname and db.existe_hostname(novo_hostname, ignorar_id=ativo.id_ativo):
            print("Já existe outro ativo com esse hostname. Escolha outro ou deixe em branco.")
            continue
        break

    novo_responsavel = ler_texto(f"Responsável [{ativo.responsavel}]: ", permitir_vazio=True)
    novo_setor = ler_texto(f"Setor/Localização [{ativo.setor}]: ", permitir_vazio=True)

    novo_tipo = None
    if ler_sim_nao("Deseja alterar o tipo de ativo? (s/n): "):
        novo_tipo = escolher_enum("Novo tipo de ativo:", TipoAtivo)

    hostname_antigo = ativo.hostname
    if novo_hostname:
        ativo.hostname = novo_hostname
    if novo_responsavel:
        ativo.responsavel = novo_responsavel
    if novo_setor:
        ativo.setor = novo_setor
    if novo_tipo is not None:
        ativo.tipo = novo_tipo

    db.reindexar_apos_edicao(ativo, hostname_antigo)
    print("\nAtivo atualizado com sucesso.")


# ------------------------------------------------------------------
# Requisito 6: Remoção de ativo (Delete)
# ------------------------------------------------------------------

def deletar_ativo(db: BancoDeDados) -> None:
    print("\n--- Remoção de ativo ---")
    id_ativo = ler_inteiro("ID do ativo a remover: ")
    ativo_existente = db.buscar_por_id(id_ativo)
    if not ativo_existente:
        print("Ativo não encontrado.")
        return

    if not ler_sim_nao(
        f"Confirma a remoção do ativo '{ativo_existente.hostname}' e de suas "
        f"{len(ativo_existente.vulnerabilidades)} vulnerabilidade(s)? (s/n): "
    ):
        print("Operação cancelada.")
        return

    ativo = db.remover(id_ativo)
    print(f"Ativo '{ativo.hostname}' e suas vulnerabilidades foram removidos.")


# ------------------------------------------------------------------
# Requisito 7: Cadastro de vulnerabilidade em ativo já existente
# ------------------------------------------------------------------

def cadastrar_vulnerabilidade(db: BancoDeDados) -> None:
    print("\n--- Cadastro de vulnerabilidade em ativo existente ---")
    id_ativo = ler_inteiro("ID do ativo: ")
    ativo = db.buscar_por_id(id_ativo)
    if not ativo:
        print("Ativo não encontrado.")
        return

    descricao = ler_texto("Descrição da vulnerabilidade: ")
    categoria = ler_texto("Categoria: ")
    severidade = escolher_enum("Severidade:", Severidade)
    status = escolher_enum("Status de tratamento:", StatusVulnerabilidade)

    ativo.vulnerabilidades.append(Vulnerabilidade(descricao, categoria, severidade, status))
    db.salvar()
    print("Vulnerabilidade cadastrada com sucesso.")


# ------------------------------------------------------------------
# Requisito 8: Visualização de vulnerabilidades de um ativo
# ------------------------------------------------------------------

def imprimir_vulnerabilidades(ativo: Ativo) -> None:
    """Mostra as vulnerabilidades numeradas (a partir de 1)."""
    for numero, vulnerabilidade in enumerate(ativo.vulnerabilidades, start=1):
        print(vulnerabilidade.formatar(numero))


def visualizar_vulnerabilidades(db: BancoDeDados) -> None:
    print("\n--- Visualização de vulnerabilidades ---")
    id_ativo = ler_inteiro("ID do ativo: ")
    ativo = db.buscar_por_id(id_ativo)
    if not ativo:
        print("Ativo não encontrado.")
        return

    print(f"\nAtivo: {ativo.hostname} (ID {ativo.id_ativo})")
    if not ativo.vulnerabilidades:
        print("Este ativo está sem vulnerabilidades registradas.")
        return

    imprimir_vulnerabilidades(ativo)


# ------------------------------------------------------------------
# Atualização e remoção de vulnerabilidades (acompanhamento do tratamento)
# ------------------------------------------------------------------

def selecionar_vulnerabilidade(db: BancoDeDados) -> Optional[Tuple[Ativo, int]]:
    """
    Pede o ID de um ativo, lista suas vulnerabilidades e pede qual delas
    o usuário quer manipular. Retorna (ativo, posição na lista) ou None.
    A posição devolvida já é o índice da lista (começa em 0).
    """
    id_ativo = ler_inteiro("ID do ativo: ")
    ativo = db.buscar_por_id(id_ativo)
    if not ativo:
        print("Ativo não encontrado.")
        return None

    print(f"\nAtivo: {ativo.hostname} (ID {ativo.id_ativo})")
    if not ativo.vulnerabilidades:
        print("Este ativo está sem vulnerabilidades registradas.")
        return None

    imprimir_vulnerabilidades(ativo)
    numero = ler_numero_da_lista("Número da vulnerabilidade: ", len(ativo.vulnerabilidades))
    return ativo, numero - 1


def atualizar_vulnerabilidade(db: BancoDeDados) -> None:
    print("\n--- Atualização de vulnerabilidade ---")
    selecao = selecionar_vulnerabilidade(db)
    if selecao is None:
        return
    ativo, indice = selecao
    vulnerabilidade = ativo.vulnerabilidades[indice]

    print("Pressione Enter sem digitar nada para manter o valor atual.")
    nova_descricao = ler_texto(f"Descrição [{vulnerabilidade.descricao}]: ", permitir_vazio=True)
    nova_categoria = ler_texto(f"Categoria [{vulnerabilidade.categoria}]: ", permitir_vazio=True)

    nova_severidade = None
    if ler_sim_nao(
        f"Alterar a severidade (atual: {rotulo_severidade(vulnerabilidade.severidade)})? (s/n): "
    ):
        nova_severidade = escolher_enum("Nova severidade:", Severidade)

    novo_status = None
    if ler_sim_nao(
        f"Alterar o status de tratamento (atual: {rotulo_status(vulnerabilidade.status)})? (s/n): "
    ):
        novo_status = escolher_enum("Novo status de tratamento:", StatusVulnerabilidade)

    # Só altera depois de coletar tudo (ver comentário em atualizar_ativo).
    if nova_descricao:
        vulnerabilidade.descricao = nova_descricao
    if nova_categoria:
        vulnerabilidade.categoria = nova_categoria
    if nova_severidade is not None:
        vulnerabilidade.severidade = nova_severidade
    if novo_status is not None:
        vulnerabilidade.status = novo_status

    db.salvar()
    print("Vulnerabilidade atualizada com sucesso.")


def remover_vulnerabilidade(db: BancoDeDados) -> None:
    print("\n--- Remoção de vulnerabilidade ---")
    selecao = selecionar_vulnerabilidade(db)
    if selecao is None:
        return
    ativo, indice = selecao

    if not ler_sim_nao("Confirma a remoção desta vulnerabilidade? (s/n): "):
        print("Operação cancelada.")
        return

    ativo.vulnerabilidades.pop(indice)
    db.salvar()
    print("Vulnerabilidade removida com sucesso.")


# ------------------------------------------------------------------
# Extra: listagem geral (facilita a demonstração/apresentação)
# ------------------------------------------------------------------

def listar_ativos(db: BancoDeDados) -> None:
    print("\n--- Lista de todos os ativos cadastrados ---")
    # Ordenado por ID: a ordem "natural" do dict é a de inserção, que muda
    # conforme cadastros e remoções vão acontecendo e fica confusa de ler.
    ativos = sorted(db.listar_todos(), key=lambda ativo: ativo.id_ativo)
    if not ativos:
        print("Nenhum ativo cadastrado.")
        return
    for ativo in ativos:
        print(
            f"ID {ativo.id_ativo:<4} | {ativo.hostname:<20} | "
            f"{ativo.tipo.name:<20} | {len(ativo.vulnerabilidades)} vulnerabilidade(s)"
        )


# ------------------------------------------------------------------
# Extra: relatório de vulnerabilidades em CSV, ordenado por severidade
# ------------------------------------------------------------------

def exportar_relatorio_vulnerabilidades(db: BancoDeDados) -> None:
    print("\n--- Exportar relatório de vulnerabilidades (CSV) ---")
    linhas = []
    for ativo in db.listar_todos():
        for vulnerabilidade in ativo.vulnerabilidades:
            linhas.append(
                {
                    "valor_severidade": vulnerabilidade.severidade.value,
                    "severidade": rotulo_severidade(vulnerabilidade.severidade),
                    "id_ativo": ativo.id_ativo,
                    "hostname": ativo.hostname,
                    "categoria": vulnerabilidade.categoria,
                    "descricao": vulnerabilidade.descricao,
                    "status": rotulo_status(vulnerabilidade.status),
                }
            )

    if not linhas:
        print("Não há vulnerabilidades cadastradas para exportar.")
        return

    # Mais graves primeiro (Crítica > Alta > Média > Baixa); em caso de
    # empate, ordena pelo ID do ativo para o relatório ficar estável.
    linhas.sort(key=lambda linha: (-linha["valor_severidade"], linha["id_ativo"]))

    nome_arquivo = ler_texto(
        "Nome do arquivo de saída [relatorio_vulnerabilidades.csv]: ",
        permitir_vazio=True,
    ) or "relatorio_vulnerabilidades.csv"

    campos = ["severidade", "id_ativo", "hostname", "categoria", "descricao", "status"]
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow({campo: linha[campo] for campo in campos})

    print(f"Relatório exportado para '{nome_arquivo}' ({len(linhas)} vulnerabilidade(s)).")


# ------------------------------------------------------------------
# Menu principal (Requisito 1)
# ------------------------------------------------------------------

def exibir_menu() -> None:
    print("\n===== Inventário de Segurança - Ativos de TI =====")
    print("1 - Cadastrar novo ativo")
    print("2 - Consultar ativo (por ID ou hostname)")
    print("3 - Atualizar ativo")
    print("4 - Remover ativo")
    print("5 - Cadastrar vulnerabilidade em ativo existente")
    print("6 - Visualizar vulnerabilidades de um ativo")
    print("7 - Listar todos os ativos")
    print("8 - Atualizar vulnerabilidade (ex.: mudar status)")
    print("9 - Remover vulnerabilidade")
    print("10 - Exportar relatório de vulnerabilidades (CSV)")
    print("0 - Sair")


def main() -> None:
    db = BancoDeDados()
    acoes = {
        1: cadastrar_ativo,
        2: buscar_ativo_interativo,
        3: atualizar_ativo,
        4: deletar_ativo,
        5: cadastrar_vulnerabilidade,
        6: visualizar_vulnerabilidades,
        7: listar_ativos,
        8: atualizar_vulnerabilidade,
        9: remover_vulnerabilidade,
        10: exportar_relatorio_vulnerabilidades,
    }

    print("Bem-vindo ao Sistema de Inventário de Segurança!")

    while True:
        # Leitura da opção do menu: Ctrl+C (KeyboardInterrupt) ou Ctrl+D
        # (EOFError) aqui significam "quero sair".
        try:
            exibir_menu()
            opcao = ler_inteiro("Escolha uma opção: ")
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando...")
            break

        if opcao == 0:
            print("Encerrando o programa. Até logo!")
            break

        acao = acoes.get(opcao)
        if acao is None:
            print("Opção inválida. Tente novamente.")
            continue

        try:
            acao(db)
        except KeyboardInterrupt:
            # Ctrl+C no meio de uma operação: cancela só a operação e volta ao
            # menu. Tudo o que já foi gravado continua na base.
            print("\nOperação cancelada. Voltando ao menu.")
        except EOFError:
            # A entrada foi encerrada (Ctrl+D ou fim de arquivo): não há como
            # continuar pedindo dados, então o programa termina normalmente.
            print("\nEntrada encerrada. Encerrando o programa...")
            break
        except Exception as erro:  # protege o loop principal de falhas inesperadas
            print(f"[Erro] Ocorreu um problema ao executar a operação: {erro}")


if __name__ == "__main__":
    main()
