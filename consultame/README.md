# Consulta.me — intranet da Clínica Consulta.me (v1)

Sistema da **Clínica Consulta.me** (fictícia): cadastro de médicos e pacientes, agenda de consultas,
receitas e envio de exames. Feito em **Django**, a partir do projeto que a turma começou em
[sistema_medico_django](https://github.com/Will-firmino/sistema_medico_django).

É a base do projeto integrador **Operação Consulta.me** — *Segurança da Informação* + *Métricas e Auditoria de Software*
(ADS · Senac Rio · 2026.2). Roteiro do projeto:
https://www.tiowill.online/segurancadainformacao/apostilas/operacao-consultame.html

> Todos os dados que vêm no banco são **fictícios** (nomes, e-mails `@exemplo.com.br`, telefones e CPFs inventados).

---

## 1. Como rodar

Precisa do **Python 3.10 ou mais novo**. Abra o terminal **na pasta `consultame`** (onde está o `manage.py`).

### Windows (PowerShell ou Prompt de Comando)

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

> Se o PowerShell reclamar de "execução de scripts desabilitada" ao ativar o venv, rode uma vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente de novo.

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abra **http://127.0.0.1:8000/** no navegador.

## 2. Logins de teste (só para o ambiente local das aulas)

| Usuário | Senha | Quem é |
|---|---|---|
| `admin` | `admin123` | Administrador (acessa também o `/admin/`) |
| `dra.ana` | `consultame123` | Dra. Ana Ribeiro — Cardiologia |
| `dr.bruno` | `consultame123` | Dr. Bruno Tavares — Clínica geral |
| `dra.carla` | `consultame123` | Dra. Carla Mendes — Pediatria |
| `recepcao` | `consultame123` | Recepção da clínica |

O banco (`db.sqlite3`) já vem com médicos, pacientes, consultas e receitas.
Para voltar ao estado inicial: `python manage.py popular --limpar`.

## 3. Mapa das pastas

```
consultame/
├── manage.py                 ← utilitário de linha de comando do Django
├── requirements.txt          ← bibliotecas do projeto (pip install -r requirements.txt)
├── db.sqlite3                ← banco de dados SQLite (com os dados de exemplo)
├── sistema/                  ← configurações do projeto (settings.py, urls.py)
├── intranet/                 ← o app da clínica
│   ├── models.py             ← Medico, Paciente, Consulta, Receita, Exame
│   ├── views.py · urls.py · forms.py · admin.py
│   ├── templates/intranet/   ← páginas HTML
│   ├── static/intranet/      ← CSS e logo
│   ├── management/commands/popular.py   ← python manage.py popular
│   └── assinatura.py · cripto.py · totp.py · bloqueio.py · upload_seguro.py   ← módulos das sprints (com TODO)
├── pki/                      ← scripts da AC da clínica e dos certificados (Sprints 1 e 2)
├── farmacia-java/            ← verificador de receitas em Java (Sprint 4)
├── backup/                   ← backup e restauração do banco (Sprint 6)
├── ioc/                      ← lista de hashes suspeitos para a Sprint 6
└── metricas/                 ← coleta da linha de base e registro de horas da equipe
```

## 4. O que cada sprint vai usar

Os arquivos marcados com `TODO` são **andaimes**: a estrutura está pronta e a equipe completa.
Eles não são usados pelo sistema até a equipe ligá-los.

| Sprint | Data | Arquivos | Instalar antes |
|---|---|---|---|
| 1 | 29/10 | `pki/criar_ac.py`, `pki/emitir_servidor.py`, `metricas/linha_de_base.py` | `pip install cryptography` |
| 2 | 05/11 | `pki/emitir_medico.py`, `intranet/assinatura.py` | — |
| 3 | 12/11 | HTTPS com o certificado do servidor (`runserver_plus`) | `pip install django-extensions Werkzeug pyOpenSSL` |
| 4 | 19/11 | `intranet/cripto.py`, `farmacia-java/VerificaReceita.java` | `pip install "django[argon2]"` e um JDK 11+ |
| 5 | 26/11 | `intranet/totp.py`, `intranet/bloqueio.py` | — |
| 6 | 03/12 | `intranet/upload_seguro.py`, `ioc/hashes_suspeitos.txt`, `backup/` | — |
| 7 | 10/12 | firewall e rede da clínica (sem código novo obrigatório) | — |

Métricas: rodem `python metricas/linha_de_base.py` no começo (linha de base) e no fim de cada sprint
(`python metricas/linha_de_base.py --rotulo sprint2`, …) e registrem as horas da equipe em
`metricas/registro_horas.csv`.

## 5. Comandos do dia a dia

```bash
python manage.py runserver            # sobe o servidor em http://127.0.0.1:8000/
python manage.py makemigrations       # depois de alterar o models.py
python manage.py migrate              # aplica as mudanças no banco
python manage.py createsuperuser      # cria outro usuário administrador
python manage.py changepassword dra.ana
python manage.py popular --limpar     # recria os dados de exemplo
python manage.py shell                # Python com o Django carregado
```
