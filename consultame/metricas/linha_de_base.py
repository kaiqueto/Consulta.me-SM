"""
Métricas — coleta da LINHA DE BASE do Consulta.me
=================================================

Ferramenta de COLETA (não de interpretação): mede o sistema "como está" para que a equipe
compare, sprint a sprint, o antes e o depois. Quem interpreta os números é a equipe,
no plano GQM e nas fichas de indicadores.

Uso (na raiz do projeto, com o venv ativo):
    python metricas/linha_de_base.py                 → mede e grava metricas/linha_de_base.csv
    python metricas/linha_de_base.py --rotulo sprint3 → grava com outro rótulo (para comparar depois)

O que é medido:
    - arquivos e linhas de código (não vazias) por tipo: .py, .html, .css, .js, .java
      (fora venv/, migrations/, media/, backup/ e __pycache__)
    - alertas de segurança de "python manage.py check --deploy"
    - rotas (URLs) do sistema
    - models do app intranet e total de campos

O CSV usa ";" e vírgula decimal — abre direto no Excel/Google Planilhas em português.
"""
import csv
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / 'metricas' / 'linha_de_base.csv'
TIPOS = ['.py', '.html', '.css', '.js', '.java']
IGNORAR = {'venv', '.venv', 'env', '__pycache__', 'migrations', 'media', 'backup', '.git', 'node_modules'}


def contar_linhas():
    """Devolve {extensão: (arquivos, linhas não vazias)}."""
    totais = {ext: [0, 0] for ext in TIPOS}
    for pasta, subpastas, arquivos in os.walk(RAIZ):
        subpastas[:] = [p for p in subpastas if p not in IGNORAR]
        for nome in arquivos:
            ext = Path(nome).suffix.lower()
            if ext in totais:
                texto = (Path(pasta) / nome).read_text(encoding='utf-8', errors='ignore')
                totais[ext][0] += 1
                totais[ext][1] += sum(1 for linha in texto.splitlines() if linha.strip())
    return totais


def alertas_check_deploy():
    """Roda 'manage.py check --deploy' e devolve (quantidade, [códigos dos alertas])."""
    proc = subprocess.run([sys.executable, 'manage.py', 'check', '--deploy'],
                          cwd=RAIZ, capture_output=True, text=True)
    saida = proc.stdout + proc.stderr
    codigos = re.findall(r'\(([a-z_]+\.[WE]\d+)\)', saida)
    return len(codigos), codigos


def rotas_e_models():
    """Liga o Django e devolve (total de rotas, models, total de campos)."""
    sys.path.insert(0, str(RAIZ))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
    import django
    django.setup()
    from django.apps import apps
    from django.urls import get_resolver, URLPattern, URLResolver

    def percorrer(padroes, prefixo=''):
        for p in padroes:
            if isinstance(p, URLResolver):
                if str(p.pattern).startswith('admin/'):
                    yield prefixo + 'admin/'          # o admin conta como uma rota só
                    continue
                yield from percorrer(p.url_patterns, prefixo + str(p.pattern))
            elif isinstance(p, URLPattern):
                yield prefixo + str(p.pattern)

    rotas = sorted(set(percorrer(get_resolver().url_patterns)))

    modelos = list(apps.get_app_config('intranet').get_models())
    campos = sum(len(m._meta.fields) for m in modelos)
    return len(rotas), len(modelos), campos


def main():
    rotulo = 'linha de base'
    if '--rotulo' in sys.argv:
        rotulo = sys.argv[sys.argv.index('--rotulo') + 1]

    linhas = contar_linhas()
    n_alertas, codigos = alertas_check_deploy()
    n_rotas, n_models, n_campos = rotas_e_models()

    medidas = [('código: ' + ext, f'{arq} arquivos', loc) for ext, (arq, loc) in linhas.items()]
    medidas += [
        ('código: total de linhas', '', sum(loc for _, loc in linhas.values())),
        ('alertas do check --deploy', ' '.join(codigos), n_alertas),
        ('rotas (URLs) do sistema', '', n_rotas),
        ('models do app intranet', '', n_models),
        ('campos nos models', '', n_campos),
    ]

    quando = datetime.now().strftime('%d/%m/%Y %H:%M')
    print(f'\nConsulta.me — {rotulo} ({quando})\n')
    print(f'{"Medida":<30} {"Valor":>7}   Detalhe')
    print('-' * 78)
    for nome, detalhe, valor in medidas:
        print(f'{nome:<30} {valor:>7}   {detalhe}')

    novo = not SAIDA.exists()
    with SAIDA.open('a', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, delimiter=';')
        if novo:
            w.writerow(['data', 'rotulo', 'medida', 'valor', 'detalhe'])
        for nome, detalhe, valor in medidas:
            w.writerow([quando, rotulo, nome, valor, detalhe])
    print(f'\nGravado em {SAIDA.relative_to(RAIZ)} (o arquivo acumula as medições — não apague).')


if __name__ == '__main__':
    main()
