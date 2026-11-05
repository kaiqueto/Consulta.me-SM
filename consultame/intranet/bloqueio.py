"""
Sprint 5 — Bloqueio por tentativas de login (contra força bruta e "password spraying")
======================================================================================

Regra da clínica: 5 falhas de login do mesmo usuário em 15 minutos → usuário bloqueado por 15 minutos.
Login certo limpa o contador.

Sugestões de implementação (escolham uma e justifiquem):
    a) cache do Django (django.core.cache) — simples, mas zera quando o servidor reinicia;
    b) um model novo (ex.: TentativaLogin com usuario, ip, quando, sucesso) — fica registrado
       e ainda serve como TRILHA DE AUDITORIA (Métricas e Auditoria agradece).

Onde ligar: numa LoginView própria (herdando de django.contrib.auth.views.LoginView), no
form_invalid/form_valid, ou com os sinais user_login_failed / user_logged_in do django.contrib.auth.

Material de apoio:
    - Apostila 05, seções "Senhas do jeito certo" (limitar tentativas) e "Fatores de autenticação"
"""

LIMITE_FALHAS = 5
JANELA_MINUTOS = 15
BLOQUEIO_MINUTOS = 15


def registrar_falha(usuario: str, ip: str) -> None:
    """Registra uma tentativa de login que falhou para `usuario` vinda de `ip`."""
    # TODO Sprint 5
    raise NotImplementedError("TODO Sprint 5: registrar a falha de login")


def esta_bloqueado(usuario: str) -> bool:
    """True se `usuario` teve LIMITE_FALHAS falhas nos últimos JANELA_MINUTOS e ainda está no período de bloqueio."""
    # TODO Sprint 5
    raise NotImplementedError("TODO Sprint 5: verificar o bloqueio")


def limpar(usuario: str) -> None:
    """Zera as falhas de `usuario` (chamado depois de um login bem-sucedido)."""
    # TODO Sprint 5
    raise NotImplementedError("TODO Sprint 5: limpar as falhas")
