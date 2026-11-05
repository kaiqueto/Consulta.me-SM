"""
Sprint 1 — A Autoridade Certificadora (AC) raiz da Clínica Consulta.me
======================================================================

A clínica vai ter a SUA PRÓPRIA AC: ela assina o certificado do servidor (Sprint 1/3)
e os certificados dos médicos (Sprint 2). Quem confia na AC confia em tudo o que ela assinou.

Uso (na raiz do projeto, com o venv ativo):
    pip install cryptography
    python pki/criar_ac.py

Gera:
    pki/ac.key  → chave privada da AC (o arquivo mais sensível do projeto: NUNCA vai para o Git)
    pki/ac.crt  → certificado raiz (público — é ele que vai ser instalado como "AC confiável")

Requisitos do certificado raiz:
    - algoritmo: ECDSA com a curva P-256 (SECP256R1) e hash SHA-256
    - titular = emissor (é AUTOassinado):  C=BR, O=Clínica Consulta.me, CN=Consulta.me AC Raiz
    - validade: 5 anos a partir de agora
    - extensões: BasicConstraints(ca=True) CRÍTICA e KeyUsage permitindo assinar certificados e LCRs

Material de apoio:
    - Apostila 04 (PKI & Certificados), seções "Padrão X.509", "Cadeia de confiança" e "Prática: chave e CSR"
    - Apostila 03 (Criptografia), seção "ECC e Diffie-Hellman"
    - Documentação: https://cryptography.io/en/latest/x509/tutorial/
"""
from datetime import datetime, timedelta, timezone

from _comum import PASTA_PKI, salvar_chave, salvar_certificado, resumo   # noqa: F401
from cryptography import x509                                            # noqa: F401
from cryptography.x509.oid import NameOID                               # noqa: F401
from cryptography.hazmat.primitives import hashes                       # noqa: F401
from cryptography.hazmat.primitives.asymmetric import ec                # noqa: F401


def gerar_chave():
    """Gera e devolve o par de chaves ECDSA P-256 da AC."""
    # TODO Sprint 1: use ec.generate_private_key(...) com a curva certa
    raise NotImplementedError("TODO Sprint 1: gerar a chave privada da AC")


def montar_nome():
    """Devolve o x509.Name da AC (C, O e CN — veja a docstring do arquivo)."""
    # TODO Sprint 1: x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME, 'BR'), ...])
    raise NotImplementedError("TODO Sprint 1: montar o nome (subject) da AC")


def criar_certificado_raiz(chave, nome):
    """Monta e assina o certificado raiz (autoassinado) e o devolve."""
    agora = datetime.now(timezone.utc)
    # TODO Sprint 1: use x509.CertificateBuilder() e encadeie:
    #   .subject_name(...)  .issuer_name(...)   → numa AC raiz, os dois são iguais. Por quê?
    #   .public_key(...)    .serial_number(x509.random_serial_number())
    #   .not_valid_before(agora)  .not_valid_after(agora + ...)
    #   .add_extension(x509.BasicConstraints(...), critical=True)
    #   .add_extension(x509.KeyUsage(...), critical=True)
    #   .sign(chave, hashes.SHA256())
    raise NotImplementedError("TODO Sprint 1: criar e assinar o certificado raiz")


if __name__ == '__main__':
    print('Criando a AC raiz da Clínica Consulta.me…')
    chave = gerar_chave()
    cert = criar_certificado_raiz(chave, montar_nome())
    # Dica: em produção a chave da AC fica cifrada — experimente passar senha=b'...' (e não a esqueça!)
    salvar_chave(chave, PASTA_PKI / 'ac.key')
    salvar_certificado(cert, PASTA_PKI / 'ac.crt')
    resumo(cert)
