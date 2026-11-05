"""
Comando:  python manage.py popular            → cria os dados de exemplo (se o banco estiver vazio)
          python manage.py popular --limpar   → apaga tudo da intranet e cria de novo

Todos os dados são FICTÍCIOS (nomes, e-mails @exemplo.com.br, telefones e CPFs inventados).
"""
import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from intranet.models import Medico, Paciente, Consulta, Receita, Exame

SENHA_EQUIPE = 'consultame123'
SENHA_ADMIN = 'admin123'

MEDICOS = [
    # usuário,     nome,    sobrenome,  crm,      especialidade
    ('dra.ana',   'Ana',   'Ribeiro',  '52101', 'CARDIOLOGIA'),
    ('dr.bruno',  'Bruno', 'Tavares',  '52187', 'CLINICA GERAL'),
    ('dra.carla', 'Carla', 'Mendes',   '52240', 'PEDIATRIA'),
]

PACIENTES = [
    ('Mariana', 'Costa'), ('Rafael', 'Lima'), ('Juliana', 'Alves'), ('Pedro', 'Henrique Souza'),
    ('Beatriz', 'Martins'), ('Lucas', 'Ferreira'), ('Camila', 'Rocha'), ('Gustavo', 'Pereira'),
    ('Larissa', 'Gomes'), ('Thiago', 'Barbosa'), ('Fernanda', 'Araújo'), ('Diego', 'Cardoso'),
]

OBSERVACOES = [
    'Paciente relata dor no peito aos esforços há 2 semanas. Solicitado ECG e ecocardiograma.',
    'Pressão arterial 15x9. Ajuste da medicação anti-hipertensiva. Retorno em 30 dias.',
    'Quadro gripal há 4 dias, sem febre no momento. Orientada hidratação e repouso.',
    'Criança com tosse seca e coriza. Ausculta pulmonar sem alterações.',
    'Check-up anual. Solicitados hemograma, glicemia e perfil lipídico.',
    'Queixa de cefaleia frequente. Investigar padrão de sono e uso de telas.',
    'Retorno com exames: colesterol LDL elevado. Iniciada orientação alimentar.',
    'Dor lombar após esforço físico. Prescrito analgésico e alongamentos.',
]

RECEITAS = [
    ('Losartana potássica 50 mg', '1 comprimido pela manhã, uso contínuo'),
    ('Dipirona 500 mg', '1 comprimido de 6/6h se dor ou febre, por até 3 dias'),
    ('Amoxicilina 500 mg', '1 cápsula de 8/8h por 7 dias'),
    ('Ibuprofeno 400 mg', '1 comprimido de 8/8h por 5 dias, após as refeições'),
    ('Paracetamol gotas 200 mg/ml', '15 gotas de 6/6h se febre'),
    ('Sinvastatina 20 mg', '1 comprimido à noite, uso contínuo'),
]


def cpf_ficticio(rnd):
    """CPF com 11 dígitos e dígitos verificadores INVÁLIDOS de propósito (não existe de verdade)."""
    base = [rnd.randint(0, 9) for _ in range(9)]
    soma = sum(d * p for d, p in zip(base, range(10, 1, -1)))
    dv1 = (soma * 10) % 11 % 10
    errado = (dv1 + 1 + rnd.randint(0, 7)) % 10   # nunca é o dígito correto
    return ''.join(map(str, base)) + str(errado) + str(rnd.randint(0, 9))


class Command(BaseCommand):
    help = 'Cria dados fictícios de exemplo para a Clínica Consulta.me'

    def add_arguments(self, parser):
        parser.add_argument('--limpar', action='store_true', help='apaga os dados da intranet antes de criar')

    def handle(self, *args, **opcoes):
        User = get_user_model()
        rnd = random.Random(2026)   # semente fixa: todo mundo gera os mesmos dados

        if opcoes['limpar']:
            Exame.objects.all().delete()
            Receita.objects.all().delete()
            Consulta.objects.all().delete()
            Paciente.objects.all().delete()
            Medico.objects.all().delete()
            User.objects.filter(username__in=['admin', 'recepcao'] + [m[0] for m in MEDICOS]).delete()
        elif Medico.objects.exists():
            self.stdout.write(self.style.WARNING('O banco já tem dados. Use --limpar para recriar.'))
            return

        # ── Usuários ──────────────────────────────────────────────────────────
        admin = User.objects.create_superuser('admin', 'ti@exemplo.com.br', SENHA_ADMIN)
        admin.first_name, admin.last_name = 'Administrador', 'TI'
        admin.save()

        recepcao = User.objects.create_user('recepcao', 'recepcao@exemplo.com.br', SENHA_EQUIPE,
                                            first_name='Recepção', last_name='Clínica')

        medicos = []
        for usuario, nome, sobrenome, crm, esp in MEDICOS:
            u = User.objects.create_user(usuario, f'{usuario}@exemplo.com.br', SENHA_EQUIPE,
                                         first_name=nome, last_name=sobrenome)
            medicos.append(Medico.objects.create(
                nome=nome, sobrenome=sobrenome, email=f'{usuario}@exemplo.com.br',
                telefone=f'(21) 3{rnd.randint(100, 999)}-{rnd.randint(1000, 9999)}',
                crm=crm, especialidade=esp, usuario=u,
            ))

        # ── Pacientes ─────────────────────────────────────────────────────────
        pacientes = []
        for nome, sobrenome in PACIENTES:
            login = f'{nome}.{sobrenome.split()[-1]}'.lower().replace('ú', 'u')
            pacientes.append(Paciente.objects.create(
                nome=nome, sobrenome=sobrenome, email=f'{login}@exemplo.com.br',
                telefone=f'(21) 9{rnd.randint(1000, 9999)}-{rnd.randint(1000, 9999)}',
                cpf=cpf_ficticio(rnd),
            ))

        # ── Consultas (outubro a dezembro de 2026) ────────────────────────────
        tz = timezone.get_current_timezone()
        inicio = datetime(2026, 10, 1, 8, 0)
        consultas = []
        for i in range(24):
            dia = inicio + timedelta(days=rnd.randint(0, 75))
            horario = timezone.make_aware(dia.replace(hour=rnd.choice([8, 9, 10, 11, 14, 15, 16]),
                                                      minute=rnd.choice([0, 30])), tz)
            if horario < timezone.make_aware(datetime(2026, 10, 28), tz):
                status = rnd.choice(['R', 'R', 'R', 'X'])
            else:
                status = rnd.choice(['A', 'A', 'C'])
            consultas.append(Consulta.objects.create(
                paciente_id=rnd.choice(pacientes), medico_id=rnd.choice(medicos), horario=horario,
                status=status, observacao=rnd.choice(OBSERVACOES) if status == 'R' else '',
            ))

        # ── Receitas das consultas já realizadas ──────────────────────────────
        realizadas = [c for c in consultas if c.status == 'R']
        for c in realizadas[:8]:
            med, pos = rnd.choice(RECEITAS)
            Receita.objects.create(consulta=c, medicamento=med, posologia=pos,
                                   emitida_em=c.horario + timedelta(minutes=25))

        self.stdout.write(self.style.SUCCESS(
            f'Pronto: {User.objects.count()} usuários, {len(medicos)} médicos, {len(pacientes)} pacientes, '
            f'{len(consultas)} consultas e {Receita.objects.count()} receitas.'
        ))
