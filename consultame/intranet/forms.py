from django import forms

from .models import Medico, Paciente, Consulta, Receita, Exame   # o ponto = "deste mesmo app"


# Lista de especialidades (formato: (valor salvo no banco, texto exibido))
ESPECIALIDADES = [
    ('CARDIOLOGIA', 'Cardiologia'),
    ('CLINICA GERAL', 'Clínica geral'),
    ('DERMATOLOGIA', 'Dermatologia'),
    ('GINECOLOGIA', 'Ginecologia'),
    ('NEUROLOGIA', 'Neurologia'),
    ('ORTOPEDIA', 'Ortopedia'),
    ('PEDIATRIA', 'Pediatria'),
]


# ─── Formulário de Médico ─────────────────────────────────────────────────────
class MedicoForm(forms.ModelForm):
    # Troca o CharField padrão por uma lista fixa de opções
    especialidade = forms.ChoiceField(
        choices=[('', 'Selecione uma especialidade')] + ESPECIALIDADES,
        label='Especialidade',
    )

    class Meta: # A classe Meta serve para configurar o form
        model = Medico # Define o model que o form representa
        fields = ['nome', 'sobrenome', 'email', 'telefone', 'crm', 'especialidade']
        labels = {'email': 'E-mail', 'crm': 'CRM'}


# ─── Formulário de Paciente ───────────────────────────────────────────────────
class PacienteForm(forms.ModelForm):
    # Aceita o CPF com ou sem pontuação (até 14 caracteres); o clean_cpf deixa só os números
    cpf = forms.CharField(max_length=14, label='CPF')

    class Meta:
        model = Paciente
        fields = ['nome', 'sobrenome', 'email', 'telefone', 'cpf', 'mensagem']
        labels = {'email': 'E-mail', 'mensagem': 'Observações'}

    def clean_cpf(self):
        # clean_<campo>: validação extra que o Django chama no form.is_valid()
        cpf = self.cleaned_data.get('cpf', '')
        return cpf.replace('.', '').replace('-', '').replace(' ', '')   # "123.456.789-01" → "12345678901"


# ─── Formulário de Consulta ───────────────────────────────────────────────────
class ConsultaForm(forms.ModelForm):
    # Campo extra (não existe no model): só filtra os médicos no navegador
    especialidade = forms.ChoiceField(
        choices=[('', 'Todas as especialidades')] + ESPECIALIDADES,
        required=False,
        label='Especialidade',
    )

    # Campo extra: a recepção digita o CPF e o sistema encontra o paciente
    cpf_paciente = forms.CharField(
        max_length=14,
        label='CPF do paciente',
        widget=forms.TextInput(attrs={'placeholder': 'Digite o CPF do paciente'}),
    )

    class Meta:
        model = Consulta
        fields = ['medico_id', 'horario', 'status', 'observacao']   # paciente_id vem do CPF
        labels = {
            'medico_id': 'Médico',
            'horario': 'Data e hora',
            'observacao': 'Observações do atendimento',
        }
        widgets = {
            # type="datetime-local" mostra o seletor de data/hora do navegador
            'horario': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'observacao': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico_id'].queryset = Medico.objects.filter(ativo=True).order_by('nome')
        self.fields['medico_id'].empty_label = 'Selecione um médico'
        self.fields['observacao'].required = False

    def clean_cpf_paciente(self):
        cpf = self.cleaned_data.get('cpf_paciente', '')
        cpf_limpo = cpf.replace('.', '').replace('-', '').replace(' ', '')
        try:
            # Devolve o OBJETO Paciente (e não o texto do CPF)
            return Paciente.objects.get(cpf=cpf_limpo, ativo=True)
        except Paciente.DoesNotExist:
            raise forms.ValidationError('Paciente com este CPF não encontrado. Cadastre o paciente primeiro.')

    def save(self, commit=True):
        instance = super().save(commit=False)                    # cria o objeto sem salvar
        instance.paciente_id = self.cleaned_data['cpf_paciente']  # o clean devolveu o Paciente
        if commit:
            instance.save()
        return instance


# ─── Formulário de Receita ────────────────────────────────────────────────────
class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['consulta', 'medicamento', 'posologia', 'observacoes']
        labels = {'posologia': 'Posologia (dose e frequência)', 'observacoes': 'Observações'}
        widgets = {'observacoes': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostra primeiro as consultas mais recentes
        self.fields['consulta'].queryset = (
            Consulta.objects.select_related('paciente_id', 'medico_id').order_by('-horario')
        )
        self.fields['consulta'].empty_label = 'Selecione a consulta'


# ─── Formulário de Exame ──────────────────────────────────────────────────────
class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = ['paciente', 'descricao', 'arquivo']
        labels = {'descricao': 'Descrição do exame', 'arquivo': 'Arquivo do exame'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(ativo=True).order_by('nome')
        self.fields['paciente'].empty_label = 'Selecione o paciente'
