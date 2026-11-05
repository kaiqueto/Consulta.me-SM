"""
Sprint 5 — Autenticação em dois fatores com TOTP (o código de 6 dígitos do app autenticador)
============================================================================================

Depois de usuário e senha (algo que você SABE), o médico digita o código que o app autenticador
do celular mostra (algo que você TEM). Padrão RFC 6238 — compatível com Google Authenticator,
Microsoft Authenticator, Authy etc.

Como funciona:
    - no cadastro do 2º fator, o sistema gera um segredo aleatório (base32) e o mostra ao usuário
      (como texto ou QR code no formato otpauth://totp/Consulta.me:<usuario>?secret=<SEGREDO>&issuer=Consulta.me)
    - a cada 30 segundos, servidor e celular calculam o mesmo código a partir do segredo e do relógio
    - o servidor aceita o código atual e, por tolerância de relógio, o da janela anterior/seguinte

Use SÓ a biblioteca padrão (hmac, hashlib, struct, base64, time, secrets).

Material de apoio:
    - Apostila 05 (Autenticação & Ameaças), seções "Fatores de autenticação" e "Códigos OTP: HOTP e TOTP"
      (lá tem o passo a passo e o vetor de teste da RFC para vocês conferirem a implementação)
"""
import base64   # noqa: F401
import hashlib  # noqa: F401
import hmac     # noqa: F401
import secrets  # noqa: F401
import struct   # noqa: F401
import time     # noqa: F401

PASSO = 30      # segundos de validade de cada código
DIGITOS = 6


def gerar_segredo() -> str:
    """Gera um segredo aleatório de 20 bytes e devolve em base32 (sem o '=' de preenchimento)."""
    # TODO Sprint 5: secrets.token_bytes(...) + base64.b32encode(...)
    raise NotImplementedError("TODO Sprint 5: gerar o segredo TOTP")


def codigo(segredo: str, instante=None) -> str:
    """
    Calcula o código TOTP de 6 dígitos para `instante` (segundos desde 1970; padrão: agora).
    contador = instante // PASSO → HMAC-SHA1(segredo, contador em 8 bytes big-endian)
    → "truncamento dinâmico" (RFC 4226) → % 10**DIGITOS → completar com zeros à esquerda.
    """
    # TODO Sprint 5
    raise NotImplementedError("TODO Sprint 5: calcular o código TOTP")


def verificar(segredo: str, codigo_digitado: str, janela: int = 1) -> bool:
    """
    True se `codigo_digitado` bater com o código do instante atual ou de até `janela` passos antes/depois.
    Use hmac.compare_digest para comparar (por que não usar == ?).
    """
    # TODO Sprint 5
    raise NotImplementedError("TODO Sprint 5: verificar o código TOTP")
