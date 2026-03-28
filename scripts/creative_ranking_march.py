#!/usr/bin/env python3
"""
Ranking de Criativos — por período (genérico)
Fonte: data/sheets/ (TIER 1)

Uso:
    python scripts/creative_ranking_march.py                    # mês atual
    python scripts/creative_ranking_march.py --date 2026-03-01 # mês específico
    python scripts/creative_ranking_march.py --since 2026-03-01 --until 2026-03-31
"""
import argparse
import os
import re
import sys
from datetime import date

import pandas as pd

# Importar da fonte única de verdade — sem reimplementar funções
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aios_utils import (
    br_num,
    parse_date_vendas,
    utm_to_ad_num,
    extract_vsl,
    extract_fq,
    cpa_status,
    CPA_ALVO, CPA_BOM, CPA_LIMITE, CPA_CORTE,
    latest_date_label,
    sheets_path,
)


# ── Loaders ───────────────────────────────────────────────────────────────────

def load_ads(alias, produto, date_label, year, month):
    """Carrega ads_{alias}.csv filtrado por ano/mês via coluna DATA (YYYY-MM-DD)."""
    path = sheets_path(alias, date_label)
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
    if 'DATA' not in df.columns:
        return pd.DataFrame()
    prefix = f'{year:04d}-{month:02d}'
    df = df[df['DATA'].astype(str).str.startswith(prefix)].copy()
    if df.empty:
        return pd.DataFrame()

    df['GASTO_N']    = df['GASTO'].apply(br_num) if 'GASTO' in df.columns else 0.0
    df['COMPRAS_N']  = pd.to_numeric(df.get('COMPRAS', 0), errors='coerce').fillna(0)
    imp_col = next((c for c in df.columns
                    if c.upper().startswith('IMPRESS') and c != 'Impressions'), None)
    df['IMPRESSOES_N'] = pd.to_numeric(df[imp_col], errors='coerce').fillna(0) if imp_col else 0
    df['CLIQUES_N']  = pd.to_numeric(df.get('CLIQUES', 0), errors='coerce').fillna(0)

    name_col = 'NOME ADS'
    if name_col not in df.columns:
        return pd.DataFrame()

    agg = df.groupby(name_col).agg(
        GASTO=('GASTO_N', 'sum'),
        COMPRAS_PLAT=('COMPRAS_N', 'sum'),
        IMPRESSOES=('IMPRESSOES_N', 'sum'),
        CLIQUES=('CLIQUES_N', 'sum'),
        DIAS_ATIVO=('DATA', 'nunique'),
    ).reset_index()
    agg.rename(columns={name_col: 'NOME ADS'}, inplace=True)
    agg['PRODUTO'] = produto
    return agg


def load_vendas(alias, produto_principal, produto_label, date_label, year, month):
    """Carrega vendas_{alias}.csv filtrado por STATUS, período e produto principal."""
    path = sheets_path(alias, date_label)
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
    if 'STATUS' not in df.columns:
        return pd.DataFrame()
    df = df[df['STATUS'].isin(['APPROVED', 'COMPLETE'])].copy()
    data_col = next((c for c in df.columns if 'DATA' in c.upper()), df.columns[0])
    df['DATA_dt'] = parse_date_vendas(df[data_col])
    df = df[(df['DATA_dt'].dt.year == year) & (df['DATA_dt'].dt.month == month)].copy()
    if 'PRODUTO' in df.columns:
        df = df[df['PRODUTO'] == produto_principal].copy()
    df['_label'] = produto_label
    return df


def build_pixel_agg(df, label):
    """Agrega vendas por AD_NUM + VSL + FQ para calcular CPA real via pixel."""
    if df.empty:
        return pd.DataFrame()
    rows = []
    for _, r in df.iterrows():
        ad_num = utm_to_ad_num(r.get('UTM_CONTENT'))
        vsl    = extract_vsl(r.get('UTM_CAMPAIGN'))
        fq     = extract_fq(r.get('UTM_CAMPAIGN'))
        val    = br_num(r.get('VALOR PAGO', 0))
        rows.append({'AD_NUM': ad_num, 'VSL': vsl, 'FQ': fq, 'VALOR': val, 'LABEL': label})
    pix = pd.DataFrame(rows)
    return pix.groupby(['AD_NUM', 'VSL', 'FQ', 'LABEL']).agg(
        VENDAS_PIX=('VALOR', 'count'),
        FAT_PIX=('VALOR', 'sum'),
    ).reset_index()


def extract_ad_num_nome(nome):
    """'AD17 [MDA]...' → 17. Sem match → None."""
    if pd.isna(nome):
        return None
    m = re.match(r'AD(\d+)\s', str(nome), re.I)
    return int(m.group(1)) if m else None


def get_status_cpa(r):
    """CPA pixel se disponível, fallback para plataforma."""
    cpa = r.get('CPA_PIX')
    if pd.isna(cpa) or cpa is None:
        cpa = r.get('CPA_PLAT')
    return cpa_status(cpa)


# ── Formatação de output ──────────────────────────────────────────────────────

def fmt_table(df, cols):
    d = df[[c for c in cols if c in df.columns]].copy()
    for c in ['GASTO', 'FAT_PIX']:
        if c in d.columns:
            d[c] = d[c].apply(lambda x: f'R${x:,.0f}' if pd.notna(x) else '-')
    for c in ['CPA_PLAT', 'CPA_PIX']:
        if c in d.columns:
            d[c] = d[c].apply(lambda x: f'R${x:.0f}' if pd.notna(x) else '-')
    for c in ['ROAS_PIX']:
        if c in d.columns:
            d[c] = d[c].apply(lambda x: f'{x:.2f}x' if pd.notna(x) else '-')
    for c in ['COMPRAS_PLAT', 'VENDAS_PIX']:
        if c in d.columns:
            d[c] = d[c].apply(lambda x: f'{int(x)}' if pd.notna(x) and x > 0 else '-')
    return d


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    today = date.today()
    parser = argparse.ArgumentParser(description='Ranking de criativos por período')
    parser.add_argument('--date', default=today.strftime('%Y-%m-%d'),
                        help='Data de referência YYYY-MM-DD (usa o mês desta data). Default: hoje.')
    parser.add_argument('--since', help='Data início customizada YYYY-MM-DD')
    parser.add_argument('--until', help='Data fim customizada YYYY-MM-DD')
    args = parser.parse_args()

    ref_date = date.fromisoformat(args.date)
    year, month = ref_date.year, ref_date.month
    date_label = latest_date_label()
    print(f"Coleta: {date_label} | Periodo: {year:04d}-{month:02d}")

    # ── 1. ADS ────────────────────────────────────────────────────────────────
    ads_mda  = load_ads('ads_mda',  'MDA',  date_label, year, month)
    ads_teus = load_ads('ads_teus', 'TEUS', date_label, year, month)
    ads_lvc  = pd.DataFrame()
    try:
        ads_lvc = load_ads('ads_lvc', 'LVC', date_label, year, month)
    except Exception:
        pass

    parts = [df for df in [ads_mda, ads_teus, ads_lvc] if not df.empty]
    if not parts:
        print("Sem dados de ads para o periodo.")
        return
    ads_all = pd.concat(parts, ignore_index=True)
    print(f"ADS: MDA={len(ads_mda)}, TEUS={len(ads_teus)}, LVC={len(ads_lvc)}")
    print(f"Gasto total: R$ {ads_all['GASTO'].sum():,.2f}")

    # ── 2. VENDAS ─────────────────────────────────────────────────────────────
    vend_mda  = load_vendas('vendas_mda',  'Mestres do Algoritmo | Profissão Youtuber', 'MDA',  date_label, year, month)
    vend_lvc  = load_vendas('vendas_lvc',  'Lucrando com Vídeos Curtos', 'LVC',  date_label, year, month)
    vend_teus = load_vendas('vendas_teus', 'Lucrando com Vídeos Curtos', 'TEUS', date_label, year, month)
    print(f"Vendas pixel (principais): MDA={len(vend_mda)}, LVC={len(vend_lvc)}, TEUS={len(vend_teus)}")

    # ── 3. UTM attribution ────────────────────────────────────────────────────
    pix_all = pd.concat(
        [build_pixel_agg(vend_mda, 'MDA'), build_pixel_agg(vend_lvc, 'LVC'), build_pixel_agg(vend_teus, 'TEUS')],
        ignore_index=True,
    )

    if not pix_all.empty:
        pix_by_ad = pix_all.groupby(['AD_NUM', 'LABEL']).agg(
            VENDAS_PIX=('VENDAS_PIX', 'sum'),
            FAT_PIX=('FAT_PIX', 'sum'),
            VSL=('VSL', lambda x: x.value_counts().index[0]),
            FQ=('FQ',  lambda x: x.value_counts().index[0]),
        ).reset_index()
    else:
        pix_by_ad = pd.DataFrame(columns=['AD_NUM', 'LABEL', 'VENDAS_PIX', 'FAT_PIX', 'VSL', 'FQ'])

    # ── 4. Extrair AD_NUM dos nomes ───────────────────────────────────────────
    ads_all['AD_NUM'] = ads_all['NOME ADS'].apply(extract_ad_num_nome)

    # ── 5. Merge ads × pixel ──────────────────────────────────────────────────
    merged = ads_all.merge(pix_by_ad, left_on=['AD_NUM', 'PRODUTO'], right_on=['AD_NUM', 'LABEL'], how='left')
    merged['CPA_PLAT'] = merged.apply(
        lambda r: round(r['GASTO'] / r['COMPRAS_PLAT'], 2) if r['COMPRAS_PLAT'] > 0 else None, axis=1)
    merged['CPA_PIX']  = merged.apply(
        lambda r: round(r['GASTO'] / r['VENDAS_PIX'], 2)
        if pd.notna(r.get('VENDAS_PIX')) and r.get('VENDAS_PIX', 0) > 0 else None, axis=1)
    merged['ROAS_PIX'] = merged.apply(
        lambda r: round(r['FAT_PIX'] / r['GASTO'], 2)
        if pd.notna(r.get('FAT_PIX')) and r.get('FAT_PIX', 0) > 0 and r['GASTO'] > 0 else None, axis=1)
    merged['STATUS'] = merged.apply(get_status_cpa, axis=1)
    merged['VSL'] = merged.get('VSL', pd.Series('N/A', index=merged.index)).fillna('N/A')
    merged['FQ']  = merged.get('FQ',  pd.Series('?',   index=merged.index)).fillna('?')
    merged['_sort'] = merged['CPA_PIX'].fillna(merged['CPA_PLAT'].fillna(9999))
    merged = merged.sort_values('_sort').drop(columns='_sort')

    # ── 6. Output ─────────────────────────────────────────────────────────────
    pd.set_option('display.max_rows', 300)
    pd.set_option('display.width', 250)
    pd.set_option('display.max_colwidth', 55)

    COLS = ['NOME ADS', 'PRODUTO', 'VSL', 'FQ', 'GASTO', 'COMPRAS_PLAT', 'CPA_PLAT',
            'VENDAS_PIX', 'CPA_PIX', 'ROAS_PIX', 'STATUS']

    print(f"\n{'='*130}")
    print(f"RANKING DE CRIATIVOS — {year:04d}-{month:02d}")
    print("Ordenado por CPA Pixel (menor = melhor). Pixel = UTM. Plataforma = Meta API.")
    print('='*130)
    print(fmt_table(merged, COLS).to_string(index=False))

    print(f"\n{'='*60}")
    print("RESUMO POR STATUS")
    print('='*60)
    status_summary = merged.groupby('STATUS').agg(
        Criativos=('NOME ADS', 'count'),
        Gasto=('GASTO', 'sum'),
        Compras_Plat=('COMPRAS_PLAT', 'sum'),
        Vendas_Pix=('VENDAS_PIX', lambda x: x.fillna(0).sum()),
    ).reset_index()
    status_summary['Gasto'] = status_summary['Gasto'].apply(lambda x: f'R${x:,.0f}')
    print(status_summary.to_string(index=False))

    print(f"\n{'='*60}")
    print("VSL BREAKDOWN — PIXEL")
    print('='*60)
    vsl_df = merged[merged['VSL'] != 'N/A'].copy()
    if not vsl_df.empty:
        vsl_sum = vsl_df.groupby(['PRODUTO', 'VSL']).agg(
            Criativos=('NOME ADS', 'count'),
            Gasto=('GASTO', 'sum'),
            Vendas_Pix=('VENDAS_PIX', lambda x: x.fillna(0).sum()),
            Fat_Pix=('FAT_PIX', lambda x: x.fillna(0).sum()),
        ).reset_index()
        vsl_sum['CPA']  = vsl_sum.apply(lambda r: f'R${r["Gasto"]/r["Vendas_Pix"]:.0f}' if r['Vendas_Pix'] > 0 else '-', axis=1)
        vsl_sum['ROAS'] = vsl_sum.apply(lambda r: f'{r["Fat_Pix"]/r["Gasto"]:.2f}x'     if r['Gasto'] > 0 else '-', axis=1)
        vsl_sum['Gasto']      = vsl_sum['Gasto'].apply(lambda x: f'R${x:,.0f}')
        vsl_sum['Vendas_Pix'] = vsl_sum['Vendas_Pix'].apply(lambda x: f'{int(x)}')
        vsl_sum['Fat_Pix']    = vsl_sum['Fat_Pix'].apply(lambda x: f'R${x:,.0f}')
        print(vsl_sum[['PRODUTO', 'VSL', 'Criativos', 'Gasto', 'Vendas_Pix', 'Fat_Pix', 'CPA', 'ROAS']].to_string(index=False))

    with_cpa = merged[merged['CPA_PIX'].notna()].copy()
    print(f"\n{'='*70}")
    print(f"TOP 10 — MENOR CPA PIXEL ({len(with_cpa)} com atribuicao)")
    print('='*70)
    print(fmt_table(with_cpa.head(10), COLS).to_string(index=False))

    print(f"\n{'='*70}")
    print("BOTTOM 10 — MAIOR CPA PIXEL (candidatos a pausa)")
    print('='*70)
    print(fmt_table(with_cpa.tail(10), COLS).to_string(index=False))

    no_pix = merged[merged['CPA_PIX'].isna()].copy()
    print(f"\n{'='*70}")
    print(f"SEM ATRIBUICAO PIXEL ({len(no_pix)} criativos)")
    print('='*70)
    print(fmt_table(no_pix, ['NOME ADS', 'PRODUTO', 'VSL', 'FQ', 'GASTO', 'COMPRAS_PLAT', 'CPA_PLAT', 'STATUS']).to_string(index=False))

    print("\nScript concluido.")


if __name__ == '__main__':
    main()
