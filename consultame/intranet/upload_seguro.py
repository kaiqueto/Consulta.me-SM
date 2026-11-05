"""
Sprint 6 — Envio seguro de exames (defesa contra malware disfarçado de exame)
=============================================================================

Hoje a tela de Exames aceita qualquer arquivo. Nesta sprint ela passa a:
    1. recusar arquivos maiores que TAMANHO_MAXIMO;
    2. conferir o TIPO REAL pelos primeiros bytes do arquivo ("assinatura" ou "magic number"),
       e não pela extensão — "exame.pdf.exe" ou um .exe renomeado para .pdf não podem passar;
       tipos permitidos: PDF, PNG e JPEG;
    3. salvar com um nome NOVO e aleatório (uuid4 + extensão correta), nunca com o nome enviado;
    4. calcular o SHA-256 do arquivo, guardar junto do exame e comparar com a lista de
       indicadores de comprometimento (IoC) em ioc/hashes_suspeitos.txt.

Pistas: o PDF começa com os bytes b'%PDF'. Descubram as assinaturas de PNG e JPEG
(pesquisem "file signature" / "magic number") e expliquem na entrega de onde tiraram.

Os objetos `f` abaixo são arquivos enviados pelo Django (UploadedFile): têm .size, .name,
.read(n), .seek(0) e .chunks().

Material de apoio:
    - Apostila 05, seções "O que é malware", "A família do malware" e "Detecção e proteção"
    - Apostila 03, seções "Funções hash" e "Hash na prática"
"""
import hashlib  # noqa: F401
import uuid     # noqa: F401

TAMANHO_MAXIMO = 5 * 1024 * 1024   # 5 MB


def validar_arquivo(f):
    """Devolve (True, '') se o arquivo pode ser aceito ou (False, 'motivo para mostrar ao usuário')."""
    # TODO Sprint 6: tamanho → tipo real pelos primeiros bytes → (não esqueça do f.seek(0) depois de ler!)
    raise NotImplementedError("TODO Sprint 6: validar o arquivo enviado")


def nome_seguro(f) -> str:
    """Devolve um nome novo e aleatório com a extensão correspondente ao TIPO REAL (ex.: '3f2c…9a.pdf')."""
    # TODO Sprint 6
    raise NotImplementedError("TODO Sprint 6: gerar o nome seguro")


def sha256_arquivo(f) -> str:
    """Calcula o SHA-256 (hexadecimal) do arquivo lendo em pedaços (f.chunks()) — arquivos grandes não cabem na memória."""
    # TODO Sprint 6
    raise NotImplementedError("TODO Sprint 6: calcular o SHA-256")
