"""
Sprint 2 — Certificado digital de cada médico (para assinar receitas)
=====================================================================

Cada médico recebe um par de chaves e um certificado emitido pela AC da clínica.
Com a chave privada, o médico assina a receita; com o certificado, qualquer um
(a farmácia, por exemplo) confere quem assinou e se o texto foi alterado.

Uso:
    python pki/emitir_medico.py dra.ana          (o argumento é o usuário do médico no sistema)

Gera:
    pki/medicos/<usuario>.key → chave privada do médico (só o médico deveria ter)
    pki/medicos/<usuario>.crt → certificado do médico, emitido pela AC

Requisitos:
    - ECDSA P-256 + SHA-256 · validade: 1 ano · BasicConstraints(ca=False)
    - titular: C=BR, O=Clínica Consulta.me, CN=<nome completo do médico>
      e o CRM em um atributo do nome (sugestão: NameOID.TITLE ou NameOID.SERIAL_NUMBER — decidam e documentem)
    - KeyUsage: digital_signature e content_commitment (não repúdio) verdadeiros; key_cert_sign falso

Material de apoio:
    - Apostila 04, seções "Tipos de certificado", "Cadeia de confiança" e "AC e AR"
    - Apostila 03, seções "O que é assinatura digital" e "Prática: assinando em Python"
"""
import os
import sys

import django

from _comum import PASTA_PKI, PASTA_MEDICOS, carregar_chave, carregar_certificado, salvar_chave, salvar_certificado, resumo  # noqa: F401
from cryptography import x509                                            # noqa: F401
from cryptography.x509.oid import NameOID                               # noqa: F401
from cryptography.hazmat.primitives import hashes                       # noqa: F401
from cryptography.hazmat.primitives.asymmetric import ec                # noqa: F401

# Liga o Django para ler o cadastro do médico no banco (nome e CRM)
sys.path.insert(0, str(PASTA_PKI.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()
from intranet.models import Medico  # noqa: E402


def emitir_certificado_medico(medico, chave_medico, chave_ac, cert_ac):
    """Monta o certificado do médico (dados vindos do model Medico), assina com a AC e devolve."""
    # TODO Sprint 2: use medico.nome, medico.sobrenome e medico.crm no titular
    raise NotImplementedError("TODO Sprint 2: emitir o certificado do médico")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Uso: python pki/emitir_medico.py <usuario-do-medico>   (ex.: dra.ana)')
    usuario = sys.argv[1]
    medico = Medico.objects.filter(usuario__username=usuario).first()
    if medico is None:
        sys.exit(f'Nenhum médico ligado ao usuário "{usuario}".')

    if not (PASTA_PKI / 'ac.key').exists():
        sys.exit('Não achei pki/ac.key — rode antes: python pki/criar_ac.py')
    chave_ac = carregar_chave(PASTA_PKI / 'ac.key')
    cert_ac = carregar_certificado(PASTA_PKI / 'ac.crt')
    # TODO Sprint 2: gere a chave do médico (ECDSA P-256)
    chave_medico = None
    cert = emitir_certificado_medico(medico, chave_medico, chave_ac, cert_ac)
    salvar_chave(chave_medico, PASTA_MEDICOS / f'{usuario}.key')
    salvar_certificado(cert, PASTA_MEDICOS / f'{usuario}.crt')
    resumo(cert)
