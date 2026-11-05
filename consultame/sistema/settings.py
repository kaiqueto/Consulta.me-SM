"""
Configurações do projeto "sistema" (Consulta.me).

Gerado pelo 'django-admin startproject' (Django 5.2) e ajustado para a clínica.
Documentação: https://docs.djangoproject.com/en/5.2/topics/settings/
"""

from pathlib import Path

# BASE_DIR é o caminho absoluto da pasta raiz do projeto
# Path(__file__) → este arquivo · .resolve() → caminho absoluto · .parent.parent → sobe duas pastas
BASE_DIR = Path(__file__).resolve().parent.parent


# ─── Configurações gerais ─────────────────────────────────────────────────────
SECRET_KEY = 'django-insecure-q7#k2v!m9x$c0nsult4m3@8r^w&e5t(1z%p6s_y+u4n)h3d*b'

DEBUG = True   # mostra a página amarela com os detalhes do erro (ajuda muito a desenvolver)

ALLOWED_HOSTS = ['*']   # libera o acesso pelo IP da máquina (ex.: celular na mesma rede)


# ─── Apps instalados ──────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',         # painel administrativo em /admin/
    'django.contrib.auth',          # autenticação (login/logout/usuários)
    'django.contrib.contenttypes',  # tipos de conteúdo (necessário para permissões)
    'django.contrib.sessions',      # sessões (mantém o usuário logado)
    'django.contrib.messages',      # mensagens flash (ex.: "Salvo com sucesso!")
    'django.contrib.staticfiles',   # arquivos estáticos (CSS, JS, imagens)
    'intranet',                     # nosso app — a intranet da clínica
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sistema.urls'


# ─── Templates ────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,   # procura templates dentro de cada app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',          # {{ request }} nos templates
                'django.contrib.auth.context_processors.auth',         # {{ user }} nos templates
                'django.contrib.messages.context_processors.messages', # mensagens flash
            ],
        },
    },
]

WSGI_APPLICATION = 'sistema.wsgi.application'


# ─── Banco de dados ───────────────────────────────────────────────────────────
# SQLite: o banco inteiro fica em um único arquivo (db.sqlite3) na raiz do projeto
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ─── Validação de senhas ──────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─── Internacionalização ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True   # guarda as datas em UTC e converte para o fuso local na hora de exibir


# ─── Arquivos estáticos (CSS, JS, imagens do projeto) ─────────────────────────
STATIC_URL = 'static/'


# ─── Arquivos de mídia (uploads: fotos, exames) ───────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ─── Autenticação ─────────────────────────────────────────────────────────────
LOGIN_URL = '/login/'          # para onde vai quem não está logado
LOGIN_REDIRECT_URL = '/'       # para onde vai depois do login
LOGOUT_REDIRECT_URL = '/login/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
