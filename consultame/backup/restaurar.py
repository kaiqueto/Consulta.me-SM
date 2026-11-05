"""
Sprint 6 — Teste de restauração (backup que nunca foi restaurado não é backup)
==============================================================================

Uso:
    python backup/restaurar.py backup/2026-12-03_1015.sqlite3

Deve:
    1. conferir o SHA-256 do arquivo com o que está no backup/MANIFESTO.txt
       (se não bater, o backup foi alterado ou corrompido → NÃO restaurar);
    2. restaurar numa cópia de teste (ex.: db_restaurado.sqlite3), nunca por cima do banco em uso;
    3. abrir a cópia e contar os registros das tabelas principais (pacientes, consultas, receitas)
       para comparar com o banco original — esses números entram no relatório da sprint.

Material de apoio:
    - Apostila 05, seção "Resposta a incidentes" (recuperação)
"""
import hashlib   # noqa: F401
import sqlite3   # noqa: F401
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MANIFESTO = RAIZ / 'backup' / 'MANIFESTO.txt'


def conferir_integridade(arquivo: Path) -> bool:
    """True se o SHA-256 do arquivo for igual ao registrado no manifesto."""
    # TODO Sprint 6
    raise NotImplementedError("TODO Sprint 6: conferir o hash do backup")


def restaurar_em_copia(arquivo: Path) -> Path:
    """Restaura o backup em RAIZ / 'db_restaurado.sqlite3' e devolve o caminho."""
    # TODO Sprint 6
    raise NotImplementedError("TODO Sprint 6: restaurar em uma cópia de teste")


def contar_registros(banco: Path) -> dict:
    """Devolve {'intranet_paciente': n, 'intranet_consulta': n, 'intranet_receita': n}."""
    # TODO Sprint 6
    raise NotImplementedError("TODO Sprint 6: contar os registros restaurados")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Uso: python backup/restaurar.py <arquivo-de-backup>')
    arq = Path(sys.argv[1])
    if not conferir_integridade(arq):
        sys.exit('ATENÇÃO: o hash não confere com o manifesto. Restauração cancelada.')
    copia = restaurar_em_copia(arq)
    print('Restaurado em', copia, '→', contar_registros(copia))
