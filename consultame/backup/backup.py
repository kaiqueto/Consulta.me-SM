"""
Sprint 6 — Backup do banco de dados (regra 3-2-1)
=================================================

Uso:
    python backup/backup.py

Deve:
    1. copiar o db.sqlite3 para backup/AAAA-MM-DD_HHMM.sqlite3 — de forma CONSISTENTE
       (com o servidor rodando, copiar o arquivo "na mão" pode pegar o banco no meio de uma escrita;
       pesquisem a API de backup do módulo sqlite3: conexao.backup(destino));
    2. acrescentar ao backup/MANIFESTO.txt uma linha "<arquivo>;<sha256>;<tamanho em bytes>;<data/hora>"
       — o SHA-256 permite provar depois que o backup não foi alterado (integridade).

Para pensar e registrar na entrega:
    - onde ficariam as 3 cópias, em 2 mídias diferentes, com 1 fora da clínica (offline ou imutável)?
    - por que um backup sempre conectado à rede não protege contra ransomware?

Material de apoio:
    - Apostila 05, seções "Ransomware em detalhe", "Detecção e proteção" e "Resposta a incidentes"
"""
import hashlib   # noqa: F401
import sqlite3   # noqa: F401
from datetime import datetime   # noqa: F401
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent      # pasta do projeto (onde fica o db.sqlite3)
PASTA_BACKUP = RAIZ / 'backup'
MANIFESTO = PASTA_BACKUP / 'MANIFESTO.txt'


def fazer_backup() -> Path:
    """Cria a cópia consistente do banco e devolve o caminho do arquivo gerado."""
    # TODO Sprint 6
    raise NotImplementedError("TODO Sprint 6: fazer o backup consistente do banco")


def registrar_no_manifesto(arquivo: Path) -> str:
    """Calcula o SHA-256 do backup, acrescenta a linha no MANIFESTO.txt e devolve o hash."""
    # TODO Sprint 6
    raise NotImplementedError("TODO Sprint 6: registrar o backup no manifesto")


if __name__ == '__main__':
    destino = fazer_backup()
    print('Backup criado:', destino)
    print('SHA-256:', registrar_no_manifesto(destino))
