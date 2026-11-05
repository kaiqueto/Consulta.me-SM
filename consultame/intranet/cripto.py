"""
Sprint 4 — Criptografia dos dados sensíveis em repouso (CPF e observações do atendimento)
=========================================================================================

Hoje o CPF dos pacientes e as observações das consultas ficam no banco como texto comum.
Nesta sprint eles passam a ser gravados CIFRADOS com AES-256-GCM (cifra autenticada).

Regras do jogo:
    - a chave tem 32 bytes (256 bits) e fica na variável de ambiente CONSULTAME_CHAVE_DADOS,
      codificada em base64 — NUNCA no código nem no Git
    - cada cifragem usa um nonce NOVO de 12 bytes (os.urandom(12)); nonce repetido com a mesma chave é falha grave
    - o texto cifrado guardado no banco = base64( nonce + cifrado ), para caber num campo de texto
    - para continuar BUSCANDO paciente pelo CPF (formulário de consulta) sem decifrar a tabela inteira,
      gravem também um "índice de busca" = HMAC-SHA256 do CPF (indice_busca)

Como gerar uma chave para o seu computador (rode uma vez e guarde o resultado):
    python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
    Windows (PowerShell):  $env:CONSULTAME_CHAVE_DADOS = "<valor>"
    macOS/Linux:           export CONSULTAME_CHAVE_DADOS="<valor>"

Material de apoio:
    - Apostila 03, seções "Algoritmos e modos", "Prática: AES em Python" e "HMAC: integridade + autenticidade"
    - Apostila 06 (Segurança de Redes), seções "Python: módulos e cryptography" e "Prática Python e boas práticas"
"""
import base64   # noqa: F401
import hmac     # noqa: F401
import hashlib  # noqa: F401
import os       # noqa: F401


def _chave() -> bytes:
    """Lê CONSULTAME_CHAVE_DADOS do ambiente e devolve os 32 bytes da chave (erro claro se faltar)."""
    # TODO Sprint 4
    raise NotImplementedError("TODO Sprint 4: carregar a chave de dados do ambiente")


def cifrar(texto: str) -> str:
    """Cifra `texto` com AES-256-GCM e devolve base64(nonce + texto cifrado) como str."""
    # TODO Sprint 4: from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    raise NotImplementedError("TODO Sprint 4: cifrar com AES-GCM")


def decifrar(token: str) -> str:
    """Faz o caminho inverso de cifrar(). Se o dado foi adulterado, o GCM acusa — tratem esse erro."""
    # TODO Sprint 4
    raise NotImplementedError("TODO Sprint 4: decifrar com AES-GCM")


def indice_busca(cpf: str) -> str:
    """
    HMAC-SHA256 do CPF (só os dígitos) em hexadecimal, para busca exata.
    Pergunta para a equipe: por que usar HMAC com chave e não um SHA-256 simples do CPF?
    (Dica: quantos CPFs possíveis existem? Quanto tempo leva para testar todos?)
    """
    # TODO Sprint 4
    raise NotImplementedError("TODO Sprint 4: índice de busca com HMAC")
