from django.contrib import admin
from intranet import models

@admin.register(models.Medico) # Registrando a classe Médico no painel admin
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'telefone', 'especialidade', 'usuario', 'ativo',)

@admin.register(models.Paciente) # Registrando a classe Paciente no painel admin
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'telefone', 'ativo',)
    search_fields = ('nome', 'sobrenome', 'cpf')   # caixa de busca do admin

@admin.register(models.Consulta) # Registrando a classe Consulta no painel admin
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente_id', 'medico_id', 'horario', 'status',)
    list_filter = ('status', 'medico_id')

@admin.register(models.Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'consulta', 'medicamento', 'emitida_em',)

@admin.register(models.Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'descricao', 'arquivo', 'enviado_em', 'enviado_por',)
