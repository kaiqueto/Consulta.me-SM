from django.urls import path

from intranet import views

# app_name define o namespace — nos templates usamos {% url 'intranet:medico-list' %}
app_name = 'intranet'

urlpatterns = [
    # ─── Painel ───────────────────────────────────────────────────────────────
    path('', views.painel, name='painel'),

    # ─── Médicos ──────────────────────────────────────────────────────────────
    path('medicos/', views.MedicoListView.as_view(), name='medico-list'),
    path('medicos/novo/', views.MedicoCreateView.as_view(), name='medico-create'),
    # <int:pk> captura o número da URL e entrega para a view como "pk" (o id)
    path('medicos/<int:pk>/editar/', views.MedicoUpdateView.as_view(), name='medico-update'),
    path('medicos/<int:pk>/excluir/', views.MedicoDeleteView.as_view(), name='medico-delete'),

    # ─── Pacientes ────────────────────────────────────────────────────────────
    path('pacientes/', views.PacienteListView.as_view(), name='paciente-list'),
    path('pacientes/novo/', views.PacienteCreateView.as_view(), name='paciente-create'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente-update'),
    path('pacientes/<int:pk>/excluir/', views.PacienteDeleteView.as_view(), name='paciente-delete'),

    # ─── Consultas ────────────────────────────────────────────────────────────
    path('consultas/', views.ConsultaListView.as_view(), name='consulta-list'),
    path('consultas/nova/', views.ConsultaCreateView.as_view(), name='consulta-create'),
    path('consultas/<int:pk>/editar/', views.ConsultaUpdateView.as_view(), name='consulta-update'),
    path('consultas/<int:pk>/excluir/', views.ConsultaDeleteView.as_view(), name='consulta-delete'),

    # ─── Receitas ─────────────────────────────────────────────────────────────
    path('receitas/', views.ReceitaListView.as_view(), name='receita-list'),
    path('receitas/nova/', views.ReceitaCreateView.as_view(), name='receita-create'),
    path('receitas/<int:pk>/', views.receita_detalhe, name='receita-detalhe'),

    # ─── Exames ───────────────────────────────────────────────────────────────
    path('exames/', views.exames, name='exames'),

    # ─── Relatórios ───────────────────────────────────────────────────────────
    path('relatorios/pacientes.csv', views.exportar_pacientes_csv, name='relatorio-pacientes'),
]
