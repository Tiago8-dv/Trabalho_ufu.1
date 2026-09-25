"""
Cores ANSI para deixar a saída do terminal mais fácil de ler.

Não usa nenhuma biblioteca externa (nada de colorama): só os códigos de
escape ANSI, suportados pela imensa maioria dos terminais modernos (Linux,
macOS, Windows Terminal / PowerShell atual). As cores são desligadas
automaticamente quando:
  - a saída não é um terminal (por exemplo, ao redirecionar para um
    arquivo com "python main.py > saida.txt"), ou
  - a variável de ambiente NO_COLOR está definida (convenção usada por
    várias ferramentas de linha de comando para pedir saída sem cor).
"""

from __future__ import annotations

import os
import sys

if os.name == "nt":
    # Truque conhecido para habilitar códigos ANSI no cmd.exe do Windows 10+.
    # Não tem efeito (e não faz mal) em terminais que já suportam ANSI.
    os.system("")

_ATIVADO = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

_RESET = "\033[0m"
_CODIGOS = {
    "verde": "32",
    "amarelo": "33",
    "vermelho": "31",
    "vermelho_forte": "1;31",
    "ciano": "36",
}

_COR_SEVERIDADE = {
    "BAIXA": "verde",
    "MEDIA": "amarelo",
    "ALTA": "vermelho",
    "CRITICA": "vermelho_forte",
}

_COR_STATUS = {
    "ABERTA": "vermelho",
    "EM_TRATAMENTO": "amarelo",
    "CORRIGIDA": "verde",
    "ACEITA_COMO_RISCO": "ciano",
}


def colorir(texto: str, cor: str) -> str:
    """Envolve 'texto' com o código ANSI de 'cor', se as cores estiverem ativas."""
    codigo = _CODIGOS.get(cor)
    if not _ATIVADO or not codigo:
        return texto
    return f"\033[{codigo}m{texto}{_RESET}"


def colorir_severidade(nome_severidade: str, texto: str) -> str:
    """nome_severidade é o .name do Enum Severidade (ex.: 'CRITICA')."""
    return colorir(texto, _COR_SEVERIDADE.get(nome_severidade, ""))


def colorir_status(nome_status: str, texto: str) -> str:
    """nome_status é o .name do Enum StatusVulnerabilidade (ex.: 'ABERTA')."""
    return colorir(texto, _COR_STATUS.get(nome_status, ""))
