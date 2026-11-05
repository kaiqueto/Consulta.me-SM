"""
Sprint 1 — Certificado do servidor da intranet (usado no HTTPS da Sprint 3)
===========================================================================

A AC da clínica (pki/ac.key + pki/ac.crt, criados com criar_ac.py) assina o certificado
do servidor web do Consulta.me. Na Sprint 3 ele será usado para ligar o HTTPS.

Uso:
    python pki/emitir_servidor.py

Gera:
    pki/servidor.key → chave privada do servidor
    pki/servidor.crt → certificado do servidor, EMITIDO PELA AC (emissor = AC, titular = servidor)

Requisitos:
    - ECDSA P-256 + SHA-256
    - titular: C=BR, O=Clínica Consulta.me, CN=localhost
    - SubjectAlternativeName com DNSName('localhost') e IPAddress(127.0.0.1)
      (o navegador confere o SAN, não o CN!)
    - validade: 1 ano · BasicConstraints(ca=False)
    - ExtendedKeyUsage: autenticação de servidor (SERVER_AUTH)

Material de apoio:
    - Apostila 04, seções "O que é um certificado", "Tipos de certificado", "Prática: chave e CSR" e "HTTPS na prática"
"""
import ipaddress                                                         # noqa: F401
import sys
from datetime import datetime, timedelta, timezone                       # noqa: F401

from _comum import PASTA_PKI, carregar_chave, carregar_certificado, salvar_chave, salvar_certificado, resumo  # noqa: F401
from cryptography import x509                                            # noqa: F401
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID          # noqa: F401
from cryptography.hazmat.primitives import hashes                       # noqa: F401
from cryptography.hazmat.primitives.asymmetric import ec                # noqa: F401


def emitir_certificado_servidor(chave_servidor, chave_ac, cert_ac):
    """Monta o certificado do servidor, assina com a chave da AC e o devolve."""
    # TODO Sprint 1: parecido com o certificado da AC, mas:
    #   - issuer_name = o subject do cert_ac
    #   - quem assina é a chave DA AC (e não a do servidor)
    #   - inclua o SubjectAlternativeName e o ExtendedKeyUsage pedidos acima
    raise NotImplementedError("TODO Sprint 1: emitir o certificado do servidor")


if __name__ == '__main__':
    if not (PASTA_PKI / 'ac.key').exists():
        sys.exit('Não achei pki/ac.key — rode antes: python pki/criar_ac.py')
    chave_ac = carregar_chave(PASTA_PKI / 'ac.key')        # se a chave da AC tiver senha: senha=b'...'
    cert_ac = carregar_certificado(PASTA_PKI / 'ac.crt')
    # TODO Sprint 1: gere a chave do servidor (ECDSA P-256)
    chave_servidor = None
    cert = emitir_certificado_servidor(chave_servidor, chave_ac, cert_ac)
    salvar_chave(chave_servidor, PASTA_PKI / 'servidor.key')
    salvar_certificado(cert, PASTA_PKI / 'servidor.crt')
    resumo(cert)
