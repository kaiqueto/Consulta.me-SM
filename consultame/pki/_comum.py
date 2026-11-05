"""
Funções de apoio usadas pelos scripts da pasta pki/ (Sprints 1 e 2).

Este arquivo já está pronto: só lê e grava arquivos PEM.
Os scripts criar_ac.py, emitir_servidor.py e emitir_medico.py é que vocês completam.
"""
import sys
from pathlib import Path

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
except ImportError:   # a biblioteca não vem com o Python
    sys.exit('Instale a biblioteca antes:  pip install cryptography')

PASTA_PKI = Path(__file__).resolve().parent          # .../consultame/pki
PASTA_MEDICOS = PASTA_PKI / 'medicos'


def salvar_chave(chave, caminho, senha=None):
    """Grava a chave privada em PEM (PKCS#8). Com `senha` (bytes), o arquivo fica cifrado."""
    cifra = (serialization.BestAvailableEncryption(senha) if senha
             else serialization.NoEncryption())
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(chave.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=cifra,
    ))
    print('  chave privada →', caminho)


def salvar_certificado(cert, caminho):
    """Grava o certificado X.509 em PEM (o texto que começa com -----BEGIN CERTIFICATE-----)."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    print('  certificado   →', caminho)


def carregar_chave(caminho, senha=None):
    """Lê uma chave privada PEM (informe `senha` em bytes se ela foi salva cifrada)."""
    return serialization.load_pem_private_key(Path(caminho).read_bytes(), password=senha)


def carregar_certificado(caminho):
    """Lê um certificado X.509 em PEM."""
    return x509.load_pem_x509_certificate(Path(caminho).read_bytes())


def resumo(cert):
    """Mostra os campos principais de um certificado — útil para conferir o que vocês geraram."""
    print('  Titular (subject):', cert.subject.rfc4514_string())
    print('  Emissor (issuer): ', cert.issuer.rfc4514_string())
    print('  Válido de', cert.not_valid_before_utc, 'até', cert.not_valid_after_utc)
    print('  Número de série:  ', hex(cert.serial_number))
    for ext in cert.extensions:
        print('  Extensão:', ext.oid._name, '(crítica)' if ext.critical else '')
