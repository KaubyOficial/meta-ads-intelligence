import pandas as pd, sys, io, re, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
SHEETS = Path('data/sheets')
date_label = '2026-03-27'
since = pd.Timestamp('2025-10-01')
until = pd.Timestamp('2026-03-26')

def parse_num(s):
    return pd.to_numeric(
        s.astype(str).str.replace('.','',regex=False).str.replace(',','.',regex=False),
        errors='coerce'
    ).fillna(0)

def cpa_label(cpa, vendas):
    if vendas == 0: return 'SEM_VENDA'
    if cpa <= 98.05:  return 'ALVO'
    if cpa <= 108.94: return 'BOM'
    if cpa <= 130.73: return 'LIMITE'
    if cpa <= 163.42: return 'CORTE'
    return 'PAUSAR'

def saturation_signal(cpm, ctr, impressoes):
    """Detecta sinais de saturação de audiência via métricas do criativo.
    Ref: docs/meta-knowledge/audience-intelligence-guide.md Seção 4
    """
    signals = []
    if impressoes < 10000:
        return 'DADOS_INSUF'
    if cpm > 35:
        signals.append('CPM_ALTO')
    if ctr < 0.5:
        signals.append('CTR_BAIXO')
    if cpm > 35 and ctr < 0.5:
        return 'SATURACAO'   # ambos sinais = saturação confirmada
    if signals:
        return '|'.join(signals)
    return 'OK'

# ADS — usar COMPRAS (pixel) para CPA por criativo, IMPRESSOES planilha, CLIQUES planilha
df_a = pd.read_csv(SHEETS / f'{date_label}_ads_mda.csv', encoding='utf-8')
df_a['_dt'] = pd.to_datetime(df_a['DATA'].astype(str), errors='coerce')
df_a = df_a[(df_a['_dt'] >= since) & (df_a['_dt'] <= until)].copy()

df_a['GASTO']   = parse_num(df_a['GASTO'])
# COMPRAS, CLIQUES, VPG, IMPRESSOES ja sao float no CSV — parse_num removeria o '.' decimal e inflaria 10x
# Usar pd.to_numeric direto para essas colunas
df_a['COMPRAS'] = pd.to_numeric(df_a['COMPRAS'], errors='coerce').fillna(0)
# Impressoes: usar col planilha (IMPRESSOES com acento), nao 'Impressions' Meta API
imp_col = next((c for c in df_a.columns if c.upper().startswith('IMPRESS') and '2' not in c and c != 'Impressions'), 'Impressions')
df_a['IMP']     = pd.to_numeric(df_a[imp_col], errors='coerce').fillna(0)
df_a['CLK']     = pd.to_numeric(df_a['CLIQUES'], errors='coerce').fillna(0) if 'CLIQUES' in df_a.columns else 0
df_a['VPG_V']   = pd.to_numeric(df_a['VPG'], errors='coerce').fillna(0)     if 'VPG'     in df_a.columns else 0

# Filtrar apenas MDA (excluir LVC rows que aparecem no sheet)
df_mda = df_a[df_a['NOME ADS'].str.contains(r'\[MDA\]', na=False)].copy()

# Agrupar por criativo
ads_g = df_mda.groupby('NOME ADS').agg(
    Gasto=('GASTO','sum'),
    Compras=('COMPRAS','sum'),
    Impressoes=('IMP','sum'),
    Cliques=('CLK','sum'),
    VPG=('VPG_V','sum'),
    Dias=('_dt','nunique')
).reset_index()
ads_g = ads_g[ads_g['Gasto'] > 0].copy()

ads_g['CPA']  = ads_g.apply(lambda r: r['Gasto']/r['Compras'] if r['Compras']>0 else 0, axis=1)
ads_g['CTR']  = (ads_g['Cliques'] / ads_g['Impressoes'] * 100).fillna(0)
ads_g['CPM']  = (ads_g['Gasto'] / ads_g['Impressoes'] * 1000).fillna(0)
ads_g['STATUS'] = ads_g.apply(lambda r: cpa_label(r['CPA'], r['Compras']), axis=1)
ads_g['SATURACAO'] = ads_g.apply(
    lambda r: saturation_signal(r['CPM'], r['CTR'], r['Impressoes']), axis=1
)

# ROAS estimado: usando ticket médio 196.10 como base para CPA
# ROAS = ticket / CPA (proxy — real ROAS usa faturamento real)
ads_g['ROAS_est'] = ads_g.apply(lambda r: 196.10/r['CPA'] if r['CPA']>0 else 0, axis=1)

# Extracto AD number
ads_g['AD_NUM'] = ads_g['NOME ADS'].apply(lambda x: int(re.match(r'AD(\d+)', str(x)).group(1)) if re.match(r'AD(\d+)', str(x)) else 0)

# Classificacao frio/quente/remarketing/advantage+ via nome
def tipo_criativo(nome):
    n = str(nome).upper()
    if 'REMARKETING' in n or '[Q]' in n: return 'RMKT'
    if 'ASC' in n: return 'ASC'
    if 'ADV+' in n or 'ADVANTAGE+' in n: return 'ADV+'
    return 'FRIO'

def campaign_type_label(tipo):
    """Retorna label de exibição para tipo de campanha Advantage+"""
    labels = {
        'ASC':  '[ASC]',
        'ADV+': '[ADV+ AUD]',
        'RMKT': '[RMKT]',
        'FRIO': '[MANUAL]',
    }
    return labels.get(tipo, '[MANUAL]')

ads_g['TIPO'] = ads_g['NOME ADS'].apply(tipo_criativo)
ads_g['TIPO_LABEL'] = ads_g['TIPO'].apply(campaign_type_label)

# RANKING completo
top = ads_g.sort_values('Gasto', ascending=False)

print('=' * 120)
print('  RANKING CRIATIVOS MDA (CORRETO) | Fonte: COMPRAS pixel | 2025-10-01 a 2026-03-26')
print('=' * 120)
print(f"{'AD':<8} {'Gasto':>11} {'Dias':>5} {'Compras':>8} {'CPA':>9} {'ROAS':>6} {'CTR':>6} {'VPG':>8}  Status     TipoCampanha")
print('-' * 120)
for _, r in top.head(40).iterrows():
    ad = f"AD{int(r['AD_NUM'])}"
    cpa_s = f"R${r['CPA']:>7,.2f}" if r['Compras']>0 else '    N/A  '
    roas_s = f"{r['ROAS_est']:>5.2f}x" if r['CPA']>0 else '  N/A '
    print(f"{ad:<8} R${r['Gasto']:>9,.2f} {int(r['Dias']):>5} {int(r['Compras']):>8,} {cpa_s} {roas_s} {r['CTR']:>5.2f}% {int(r['VPG']):>8,}  {r['STATUS']:<10} {r['TIPO_LABEL']}")

print()
print('POR STATUS:')
total_gasto = ads_g['Gasto'].sum()
for st in ['ALVO','BOM','LIMITE','CORTE','PAUSAR','SEM_VENDA']:
    ds = ads_g[ads_g['STATUS']==st]
    if len(ds)==0: continue
    g=ds['Gasto'].sum(); v=ds['Compras'].sum(); n=len(ds)
    pct_g = g/total_gasto*100
    print(f"  [{st:<10}] {n:>3} criat | Gasto R${g:>9,.0f} ({pct_g:>5.1f}%) | Compras pixel {v:>6,}")

print()
print('POR TIPO DE CAMPANHA (Advantage+ vs Manual):')
for tp in ['[ASC]', '[ADV+ AUD]', '[MANUAL]', '[RMKT]']:
    dt = ads_g[ads_g['TIPO_LABEL'] == tp]
    if len(dt) == 0: continue
    g = dt['Gasto'].sum(); v = dt['Compras'].sum()
    cpa_tp = g/v if v > 0 else 0
    pct = g/total_gasto*100
    cpa_s = f"R${cpa_tp:,.2f}" if v > 0 else 'N/A'
    print(f"  {tp:<14} {len(dt):>3} criat | Gasto R${g:>9,.0f} ({pct:>5.1f}%) | Compras {v:>5,} | CPA médio {cpa_s}")

print()
print('TOP 10 MELHORES CPA (min 10 compras, sem Copia):')
best = ads_g[(ads_g['Compras']>=10) & (ads_g['CPA']>0) & (~ads_g['NOME ADS'].str.contains('pia|COPIA', case=False, na=False))].sort_values('CPA').head(10)
for _, r in best.iterrows():
    ad = f"AD{int(r['AD_NUM'])}"
    hook = r['NOME ADS'].split('VENDA - ')[-1][:45] if 'VENDA - ' in r['NOME ADS'] else r['NOME ADS'][:45]
    print(f"  {ad:<8} CPA R${r['CPA']:>7,.2f} [{r['STATUS']:<6}] | ROAS_est {r['ROAS_est']:.2f}x | {int(r['Compras']):>4} compras | CTR {r['CTR']:.2f}% | {hook}")

print()
print('TOP 5 PIORES CPA (gasto > R$5k, sem Copia):')
worst = ads_g[(ads_g['Gasto']>5000) & (~ads_g['NOME ADS'].str.contains('pia|COPIA', case=False, na=False))].sort_values('CPA', ascending=False).head(5)
for _, r in worst.iterrows():
    ad = f"AD{int(r['AD_NUM'])}"
    hook = r['NOME ADS'].split('VENDA - ')[-1][:40] if 'VENDA - ' in r['NOME ADS'] else r['NOME ADS'][:40]
    cpa_s = f"R${r['CPA']:,.2f}" if r['Compras']>0 else 'SEM COMPRA'
    print(f"  {ad:<8} CPA {cpa_s:<12} | ROAS_est {r['ROAS_est']:.2f}x | Gasto R${r['Gasto']:>8,.0f} | {int(r['Compras']):>4} compras | {hook}")

print()
print('ALERTAS DE AUDIÊNCIA / SATURAÇÃO:')
saturados = ads_g[ads_g['SATURACAO'] == 'SATURACAO']
cpm_alto   = ads_g[ads_g['SATURACAO'] == 'CPM_ALTO']
ctr_baixo  = ads_g[ads_g['SATURACAO'] == 'CTR_BAIXO']
if len(saturados):
    print(f"  🔴 SATURAÇÃO CONFIRMADA (CPM alto + CTR baixo): {len(saturados)} criativos")
    for _, r in saturados.iterrows():
        print(f"     AD{int(r['AD_NUM']):<4} CPM R${r['CPM']:,.2f} | CTR {r['CTR']:.2f}% | {r['TIPO_LABEL']}")
if len(cpm_alto):
    print(f"  🟡 CPM ALTO (> R$35): {len(cpm_alto)} criativos — possível saturação de audiência")
if len(ctr_baixo):
    print(f"  🟡 CTR BAIXO (< 0.5%): {len(ctr_baixo)} criativos — revisar hook ou audiência")
if not len(saturados) and not len(cpm_alto) and not len(ctr_baixo):
    print("  ✅ Sem sinais críticos de saturação de audiência")

print()
print('SUMMARY:')
print(f"  Total criativos MDA ativos: {len(ads_g)}")
print(f"  Total gasto ads:    R${ads_g['Gasto'].sum():,.2f}")
print(f"  Total compras px:   {ads_g['Compras'].sum():,.0f}")
print(f"  CPA medio global:   R${ads_g['Gasto'].sum()/ads_g['Compras'].sum():,.2f}")
print(f"  Criativos ALVO+BOM: {len(ads_g[ads_g['STATUS'].isin(['ALVO','BOM'])])}")
print(f"  Criativos PAUSAR:   {len(ads_g[ads_g['STATUS']=='PAUSAR'])}")
print(f"  Criativos SEM VENDA: {len(ads_g[ads_g['STATUS']=='SEM_VENDA'])}")

# Save updated artifact
os.makedirs('.ai', exist_ok=True)
ranking = []
for _, r in ads_g.sort_values('Gasto', ascending=False).iterrows():
    ranking.append({
        'ad': f"AD{int(r['AD_NUM'])}",
        'nome': r['NOME ADS'],
        'tipo': r['TIPO'],
        'tipo_label': r['TIPO_LABEL'],
        'gasto': round(float(r['Gasto']),2),
        'dias': int(r['Dias']),
        'compras_pixel': int(r['Compras']),
        'cpa': round(float(r['CPA']),2),
        'roas_est': round(float(r['ROAS_est']),4),
        'ctr': round(float(r['CTR']),2),
        'vpg': int(r['VPG']),
        'status': r['STATUS'],
        'saturacao': r['SATURACAO']
    })

por_status = {}
for st in ['ALVO','BOM','LIMITE','CORTE','PAUSAR','SEM_VENDA']:
    ds = ads_g[ads_g['STATUS']==st]
    por_status[st] = {'n': int(len(ds)), 'gasto': round(float(ds['Gasto'].sum()),2), 'compras': int(ds['Compras'].sum())}

artifact = {
    'workflow': 'meta-ads-intelligence',
    'etapa': 4,
    'produto': 'MDA',
    'periodo': {'since': '2025-10-01', 'until': '2026-03-26'},
    'generated_at': '2026-03-27',
    'metodologia': 'COMPRAS coluna planilha (pixel) — fonte correta para CPA por criativo',
    'correcao': 'v1 usou UTM_CONTENT join (70.5% coverage) — CPA calculado incorretamente. v2 usa COMPRAS pixel.',
    'rules_applied': ['cpa-targets-r196', 'compras-pixel-por-criativo'],
    'summary': {
        'total_criativos': len(ads_g),
        'gasto_total': round(float(ads_g['Gasto'].sum()),2),
        'compras_total_pixel': int(ads_g['Compras'].sum()),
        'cpa_medio': round(float(ads_g['Gasto'].sum()/ads_g['Compras'].sum()),2) if ads_g['Compras'].sum()>0 else 0,
    },
    'por_status': por_status,
    'ranking': ranking
}
with open('.ai/2026-03-27-creatives.json', 'w', encoding='utf-8') as f:
    json.dump(artifact, f, ensure_ascii=False, indent=2)
print()
print('Artifact atualizado: .ai/2026-03-27-creatives.json')
