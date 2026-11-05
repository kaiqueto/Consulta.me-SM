import csv
import json

from django.contrib import messages                          # mensagens flash ("Salvo com sucesso!")
from django.contrib.auth.decorators import login_required    # exige login em views de função
from django.contrib.auth.mixins import LoginRequiredMixin    # exige login em class-based views
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy                         # gera a URL a partir do name
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Medico, Paciente, Consulta, Receita, Exame
from .forms import MedicoForm, PacienteForm, ConsultaForm, ReceitaForm, ExameForm, ESPECIALIDADES


# GET, POST, PUT, DELETE
# REQUEST <-> RESPONSE
# RENDER -> RENDERIZAR

# ─── Painel (página inicial depois do login) ──────────────────────────────────
@login_required   # sem login → redireciona para LOGIN_URL (/login/)
def painel(request):
    hoje = timezone.localdate()
    contexto = {
        'total_medicos': Medico.objects.filter(ativo=True).count(),
        'total_pacientes': Paciente.objects.filter(ativo=True).count(),
        'consultas_hoje': Consulta.objects.filter(horario__date=hoje).count(),
        'total_receitas': Receita.objects.count(),
        # as 5 próximas consultas a partir de agora
        'proximas': Consulta.objects.select_related('paciente_id', 'medico_id')
                                    .filter(horario__gte=timezone.now()).order_by('horario')[:5],
    }
    return render(request, 'intranet/painel.html', contexto)


# Mixin com o título da página: evita repetir o get_context_data em todas as views
class TituloMixin:
    titulo = ''

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = self.titulo
        return ctx


# ─── Médicos ──────────────────────────────────────────────────────────────────
# LoginRequiredMixin deve ser o PRIMEIRO da herança
class MedicoListView(LoginRequiredMixin, ListView):
    model = Medico
    template_name = 'intranet/medicos/listagem.html'
    context_object_name = 'medicos'   # nome da lista no template ({{ medicos }})

    def get_queryset(self):
        return Medico.objects.filter(ativo=True).order_by('nome')


class MedicoCreateView(LoginRequiredMixin, TituloMixin, CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'intranet/medicos/formulario.html'
    success_url = reverse_lazy('intranet:medico-list')
    titulo = 'Cadastro de médico'


class MedicoUpdateView(LoginRequiredMixin, TituloMixin, UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'intranet/medicos/formulario.html'   # reaproveita o template do cadastro
    success_url = reverse_lazy('intranet:medico-list')
    titulo = 'Editar médico'


class MedicoDeleteView(LoginRequiredMixin, TituloMixin, DeleteView):
    model = Medico
    template_name = 'intranet/confirmar_exclusao.html'
    success_url = reverse_lazy('intranet:medico-list')
    titulo = 'Excluir médico'


# ─── Pacientes ────────────────────────────────────────────────────────────────
class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'intranet/pacientes/listagem.html'
    context_object_name = 'pacientes'

    def get_queryset(self):
        return Paciente.objects.filter(ativo=True).order_by('nome')


class PacienteCreateView(LoginRequiredMixin, TituloMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'intranet/pacientes/formulario.html'
    success_url = reverse_lazy('intranet:paciente-list')
    titulo = 'Cadastro de paciente'


class PacienteUpdateView(LoginRequiredMixin, TituloMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'intranet/pacientes/formulario.html'
    success_url = reverse_lazy('intranet:paciente-list')
    titulo = 'Editar paciente'


class PacienteDeleteView(LoginRequiredMixin, TituloMixin, DeleteView):
    model = Paciente
    template_name = 'intranet/confirmar_exclusao.html'
    success_url = reverse_lazy('intranet:paciente-list')
    titulo = 'Excluir paciente'


# ─── Consultas ────────────────────────────────────────────────────────────────
class ConsultaListView(LoginRequiredMixin, ListView):
    model = Consulta
    template_name = 'intranet/consultas/listagem.html'
    context_object_name = 'consultas'

    def get_queryset(self):
        # select_related faz o JOIN com paciente e médico numa query só (evita o problema N+1)
        return Consulta.objects.select_related('paciente_id', 'medico_id').order_by('-horario')


def _medicos_json():
    # Lista de médicos em JSON para o JavaScript do formulário filtrar por especialidade
    medicos = list(
        Medico.objects.filter(ativo=True).order_by('nome').values('id', 'nome', 'sobrenome', 'especialidade')
    )
    return json.dumps(medicos, ensure_ascii=False)


class ConsultaFormMixin(TituloMixin):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['medicos_json'] = _medicos_json()
        ctx['especialidades'] = ESPECIALIDADES
        return ctx


class ConsultaCreateView(LoginRequiredMixin, ConsultaFormMixin, CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'intranet/consultas/formulario.html'
    success_url = reverse_lazy('intranet:consulta-list')
    titulo = 'Agendamento de consulta'


class ConsultaUpdateView(LoginRequiredMixin, ConsultaFormMixin, UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'intranet/consultas/formulario.html'
    success_url = reverse_lazy('intranet:consulta-list')
    titulo = 'Editar consulta'

    def get_initial(self):
        # pré-preenche o CPF e a especialidade na tela de edição
        initial = super().get_initial()
        obj = self.get_object()
        initial['cpf_paciente'] = obj.paciente_id.cpf
        initial['especialidade'] = obj.medico_id.especialidade
        initial['horario'] = timezone.localtime(obj.horario).strftime('%Y-%m-%dT%H:%M')
        return initial


class ConsultaDeleteView(LoginRequiredMixin, TituloMixin, DeleteView):
    model = Consulta
    template_name = 'intranet/confirmar_exclusao.html'
    success_url = reverse_lazy('intranet:consulta-list')
    titulo = 'Excluir consulta'


# ─── Receitas ─────────────────────────────────────────────────────────────────
class ReceitaListView(LoginRequiredMixin, ListView):
    model = Receita
    template_name = 'intranet/receitas/listagem.html'
    context_object_name = 'receitas'

    def get_queryset(self):
        return (Receita.objects
                .select_related('consulta__paciente_id', 'consulta__medico_id')   # __ atravessa as FKs
                .order_by('-emitida_em'))


class ReceitaCreateView(LoginRequiredMixin, TituloMixin, CreateView):
    model = Receita
    form_class = ReceitaForm
    template_name = 'intranet/receitas/formulario.html'
    titulo = 'Nova receita'

    def get_initial(self):
        # /receitas/nova/?consulta=7 já deixa a consulta escolhida
        initial = super().get_initial()
        if self.request.GET.get('consulta'):
            initial['consulta'] = self.request.GET['consulta']
        return initial

    def get_success_url(self):
        messages.success(self.request, 'Receita emitida.')
        return reverse_lazy('intranet:receita-detalhe', args=[self.object.pk])


@login_required
def receita_detalhe(request, pk):
    # Página da receita pronta para imprimir
    receita = get_object_or_404(
        Receita.objects.select_related('consulta__paciente_id', 'consulta__medico_id'), pk=pk
    )
    return render(request, 'intranet/receitas/imprimir.html', {'receita': receita})


# ─── Exames ───────────────────────────────────────────────────────────────────
@login_required
def exames(request):
    # A mesma página mostra o formulário de envio (POST) e a lista dos exames (GET)
    if request.method == 'POST':
        # request.FILES traz os arquivos enviados pelo <input type="file">
        form = ExameForm(request.POST, request.FILES)
        if form.is_valid():
            exame = form.save(commit=False)
            exame.enviado_por = request.user
            exame.save()
            messages.success(request, 'Exame enviado com sucesso.')
            return redirect('intranet:exames')
    else:
        form = ExameForm()

    lista = Exame.objects.select_related('paciente', 'enviado_por').order_by('-enviado_em')
    return render(request, 'intranet/exames/listagem.html', {'form': form, 'exames': lista})


# ─── Relatórios ───────────────────────────────────────────────────────────────
# Exporta os pacientes para a planilha da recepção (abre direto no Excel)
def exportar_pacientes_csv(request):
    resposta = HttpResponse(content_type='text/csv; charset=utf-8')
    resposta['Content-Disposition'] = 'attachment; filename="pacientes.csv"'
    resposta.write('﻿')   # BOM: faz o Excel reconhecer os acentos

    escritor = csv.writer(resposta, delimiter=';')
    escritor.writerow(['id', 'nome', 'sobrenome', 'cpf', 'email', 'telefone', 'cadastro'])
    for p in Paciente.objects.order_by('nome'):
        escritor.writerow([
            p.id, p.nome, p.sobrenome, p.cpf, p.email, p.telefone,
            timezone.localtime(p.criacao_data).strftime('%d/%m/%Y'),
        ])
    return resposta
