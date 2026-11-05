from django.conf import settings  # para referenciar o modelo de usuário do Django (settings.AUTH_USER_MODEL)
from django.utils import timezone  # Importação do módulo timezone que traz datas e horários.

from django.db import models


# ─── TABELA: medico ───────────────────────────────────────────────────────────
# Modelo do médico, com nome, email, telefone, crm, especialidade
class Medico(models.Model):
    # Atributos = características = variáveis
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)
    email = models.EmailField()
    criacao_data = models.DateTimeField(default=timezone.now)
    telefone = models.CharField(max_length=15)
    crm = models.CharField(max_length=6)
    especialidade = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)
    mensagem = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='img/%Y/%m', blank=True)

    # Login do médico no sistema (OneToOne: cada usuário é, no máximo, um médico)
    # SET_NULL: se o usuário for apagado, o cadastro do médico continua existindo
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='medico',
    )

    # Métodos = ações = funções
    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


# ─── TABELA: paciente ─────────────────────────────────────────────────────────
# Modelo do paciente, com nome, email, telefone, cpf
class Paciente(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11)   # 11 dígitos, sem pontos e traço
    criacao_data = models.DateTimeField(default=timezone.now)
    mensagem = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='img/%Y/%m', blank=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


# ─── TABELA: consulta ─────────────────────────────────────────────────────────
class Consulta(models.Model):
    # ForeignKey = relacionamento "muitos para um" (N:1)
    # on_delete=CASCADE: se o paciente/médico for apagado, as consultas dele também são
    paciente_id = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico_id = models.ForeignKey(Medico, on_delete=models.CASCADE)
    horario = models.DateTimeField(default=timezone.now)
    observacao = models.TextField(blank=True)   # anotações do atendimento
    status = models.CharField(
        default='A',
        max_length=1,
        choices=(
            ('A', 'Agendada'),
            ('X', 'Cancelada'),
            ('C', 'Confirmada'),
            ('R', 'Realizada')
        )
    )

    def __str__(self):
        # timezone.localtime: converte o horário (guardado em UTC) para o fuso da clínica
        quando = timezone.localtime(self.horario).strftime('%d/%m/%Y %H:%M')
        return f'{quando} — {self.paciente_id} com {self.medico_id}'


# ─── TABELA: receita ──────────────────────────────────────────────────────────
# Receita emitida pelo médico ao final de uma consulta
class Receita(models.Model):
    # related_name='receitas': permite fazer consulta.receitas.all()
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='receitas')
    medicamento = models.CharField(max_length=120)
    posologia = models.CharField(max_length=200)   # dose e frequência (ex.: "1 comprimido de 8/8h por 7 dias")
    observacoes = models.TextField(blank=True)
    emitida_em = models.DateTimeField(default=timezone.now)

    # Reservados para a receita digital (assinatura e certificado do médico)
    assinatura = models.TextField(blank=True)
    certificado = models.TextField(blank=True)

    def __str__(self):
        return f'Receita #{self.pk} — {self.medicamento}'


# ─── TABELA: exame ────────────────────────────────────────────────────────────
# Arquivo de exame enviado pela recepção (PDF, imagem…)
class Exame(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='exames')
    descricao = models.CharField(max_length=120)
    arquivo = models.FileField(upload_to='exames/%Y/%m')   # salva em media/exames/ANO/MES/
    enviado_em = models.DateTimeField(default=timezone.now)
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )

    def __str__(self):
        return f'{self.descricao} — {self.paciente}'
