"""
Sprint 2 — Assinatura digital das receitas
==========================================

Objetivo: a receita emitida no Consulta.me passa a ser ASSINADA com a chave privada do médico
(gerada em pki/emitir_medico.py). Qualquer alteração no texto depois da assinatura — uma dose,
um medicamento, uma vírgula — faz a verificação falhar.

Ideia geral:
    1. dados_canonicos(receita) → transforma a receita SEMPRE nos mesmos bytes
       (mesma ordem de campos, mesmos separadores, UTF-8). Sem isso, a mesma receita
       poderia gerar bytes diferentes e a assinatura "quebraria" sem ninguém ter alterado nada.
    2. assinar(...)  → ECDSA com SHA-256 sobre esses bytes; guarda em Receita.assinatura (base64)
                       e o certificado do médico em Receita.certificado (PEM)
    3. verificar(...) → confere (a) se o certificado do médico foi emitido pela AC da clínica e
                        está no prazo de validade e (b) se a assinatura bate com os bytes.

Exportação para a "farmácia" (Sprint 4, verificador em Java), 3 arquivos:
    receita-<id>.txt  → exatamente os bytes de dados_canonicos(receita)
    receita-<id>.sig  → a assinatura em base64
    medico.crt        → o certificado do médico (PEM)

Este módulo ainda NÃO é usado pelas views — ligar a assinatura na tela de receitas faz parte da sprint.

Material de apoio:
    - Apostila 03, seções "O que é assinatura digital", "Como assinar e verificar" e "Prática: assinando em Python"
    - Apostila 04, seção "Cadeia de confiança"
"""
import base64   # noqa: F401
import json     # noqa: F401


def dados_canonicos(receita) -> bytes:
    """
    Devolve os bytes canônicos da receita.

    Inclua, no mínimo: id da receita, data de emissão (ISO 8601), nome e CRM do médico,
    nome do paciente, medicamento, posologia e observações.
    Use json.dumps(..., sort_keys=True, separators=(',', ':'), ensure_ascii=False) e codifique em UTF-8.
    Pergunta para a equipe: o CPF do paciente deve entrar? Por quê (pensem na LGPD)?
    """
    # TODO Sprint 2
    raise NotImplementedError("TODO Sprint 2: gerar os bytes canônicos da receita")


def assinar(receita, chave_privada_pem: bytes) -> str:
    """
    Assina dados_canonicos(receita) com a chave privada do médico (PEM)
    e devolve a assinatura (ECDSA SHA-256, formato DER) codificada em base64 (str).
    """
    # TODO Sprint 2: serialization.load_pem_private_key(...) e chave.sign(dados, ec.ECDSA(hashes.SHA256()))
    raise NotImplementedError("TODO Sprint 2: assinar a receita")


def verificar(dados: bytes, assinatura_b64: str, certificado_pem: bytes, ac_pem: bytes) -> bool:
    """
    Devolve True somente se:
      - o certificado do médico foi emitido (assinado) pela AC da clínica (ac_pem);
      - o certificado está dentro do prazo de validade;
      - a assinatura confere com os dados.
    Em qualquer outro caso, devolve False (não deixe a exceção "vazar" para quem chamou).
    """
    # TODO Sprint 2: dica — cert_medico.verify_directly_issued_by(cert_ac) e
    #                public_key().verify(assinatura, dados, ec.ECDSA(hashes.SHA256()))
    raise NotImplementedError("TODO Sprint 2: verificar a assinatura")
