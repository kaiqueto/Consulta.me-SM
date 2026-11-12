# Consulta.me-SM
Equipe:
- Líder Técnico: Ellen
- Guardião das Métricas: Victor
- Auditor: Kaique
- Documentador: Yasmin


# ista de Erros

## Admin:

- É possível cadastrar o número do paciente com dígitos faltantes
- É possível cadastrar o CRM do médico com dígitos faltante
- É possível colocar o cpf sem números
- É possível adicionar Médicos com o mesmo CRM
- É possível adicionar o CRM do médico com letras
- É possível adicionar pacientes com CPFs iguais
- É possível adicionar letras no número de cadastro
- É possível enviar exames

## Sistema

- Aceita duas consultas do mesmo paciente no mesmo horário sistema permite que você cadastre o médico como paciente e que ele se atenda
- CPF do paciente visível no banco de dados (dado sensível não criptografado)
- É possível retornar a página anterior depois de sair (deslogar) do sistema

## Médicos

- Médicos podem mudar a receitas de outros médicos
- Podem excluir a consulta agendada de outro médico
- Consegue visualizar consultas que não lhe pertence
- dr.bruno → consegue criar uma receita médica com consultas de outros médicos
- Pode agendar consulta
- Pode exportar lista com dados sensíveis de pacientes
- Pode ver e editar médicos do sistema
- Pode editar e excluir os pacientes

## Recepção

- Pode add um novo paciente com cpf incompleto
- Pode adicionar uma receita para um paciente
- Pode excluir paciente
- Página de receita: dosagem sem número

## Melhorias

- Permitir que somente os médicos alterem na Receita
- Criar logs para cada edição realizada em consulta e receita no sistema’
- Limitar o acesso do ADM a procedimentos realizados por médicos(cadastrar exames, receitas)
- Limitar o acesso da Recepção a somente gerenciar consultas
- Recepção solicita receita ao médico, não possui acesso direto
- Recepçao não deve excluir paciente
- Médico solicita pedido á recepção que agenda consulta de paciente
- Só quem pode exportar a informações de pacientes é o admin
- Limitar a edição e exclusão de pacientes somentes a admins
