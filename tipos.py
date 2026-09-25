"""
Módulo de enumerações usadas pelo sistema de inventário de segurança.

Atende ao Requisito 2 da Tabela 1: lista de tipos de ativos de TI com
pelo menos 4 categorias, implementada como estrutura de enumeração (Enum),
cada uma associada a um código inteiro para referência no sistema.
"""

from __future__ import annotations  # garante compatibilidade com Python 3.8+

from enum import Enum


class TipoAtivo(Enum):
    """Tipos de ativos de TI reconhecidos pelo sistema."""
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    SOFTWARE_LICENCIADO = 4
    APLICACAO_WEB = 5
    BANCO_DE_DADOS = 6
    IMPRESSORA_REDE = 7
    ESTACAO_TRABALHO = 8


class Severidade(Enum):
    """Escala de severidade de uma vulnerabilidade (Requisito 7)."""
    BAIXA = 1
    MEDIA = 2
    ALTA = 3
    CRITICA = 4


class StatusVulnerabilidade(Enum):
    """Status de tratamento de uma vulnerabilidade (Requisito 7)."""
    ABERTA = 1
    EM_TRATAMENTO = 2
    CORRIGIDA = 3
    ACEITA_COMO_RISCO = 4


# Rótulos "amigáveis" em português para exibição ao usuário. Mantemos os
# nomes internos do Enum em maiúsculas/sem acento (boa prática de código),
# mas exibimos ao usuário um texto mais natural.
_ROTULOS_SEVERIDADE = {
    Severidade.BAIXA: "Baixa",
    Severidade.MEDIA: "Média",
    Severidade.ALTA: "Alta",
    Severidade.CRITICA: "Crítica",
}

_ROTULOS_STATUS = {
    StatusVulnerabilidade.ABERTA: "Aberta",
    StatusVulnerabilidade.EM_TRATAMENTO: "Em tratamento",
    StatusVulnerabilidade.CORRIGIDA: "Corrigida",
    StatusVulnerabilidade.ACEITA_COMO_RISCO: "Aceita como risco",
}


def rotulo_severidade(severidade: Severidade) -> str:
    """Retorna o texto amigável correspondente a uma Severidade."""
    return _ROTULOS_SEVERIDADE[severidade]


def rotulo_status(status: StatusVulnerabilidade) -> str:
    """Retorna o texto amigável correspondente a um StatusVulnerabilidade."""
    return _ROTULOS_STATUS[status]
