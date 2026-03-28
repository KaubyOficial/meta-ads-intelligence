#!/usr/bin/env python3
"""
Meta Ads Intelligence -- Quick Status Panel
Exibe painel de performance consolidado direto no terminal.

Comandos (*):
    *status          -> hoje/ontem
    *semana          -> semana atual (seg-hoje)
    *pl              -> P&L com reembolsos + breakdown orderbumps (receita real)
    *lucro           -> alias de *pl (lucro liquido real do periodo)
    *criativos       -> ranking de criativos
    *pausar          -> alertas de corte urgente
    *budget          -> distribuicao de orcamento por fase (F1/F2/F3/RMKT em %)
    *origem          -> vendas por canal de origem (Facebook/Bio/Hotmart/Manychat/etc)
    *checkout        -> funil VPV -> IC -> Venda com alertas automaticos

Uso direto:
    python scripts/quick_status.py
    python scripts/quick_status.py --period week
    python scripts/quick_status.py --period month
    python scripts/quick_status.py --since 2026-03-10 --until 2026-03-18
    python scripts/quick_status.py --mode creatives
    python scripts/quick_status.py --mode alerts
    python scripts/quick_status.py --mode pl
    python scripts/quick_status.py --mode budget
    python scripts/quick_status.py --mode origem
    python scripts/quick_status.py --mode checkout
"""

import argparse
import sys
import os
import re
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SHEETS = ROOT / "data" / "sheets"

# analyst-rules.md Secao 1 — CPA targets (ticket R$196,10)
# NUNCA usar TICKET_MEDIO como multiplicador de receita — apenas para CPA targets
TICKET_MEDIO = 196.10
CPA_ALVO    = 98.05
CPA_BOM     = 108.94
CPA_LIMITE  = 130.73
CPA_CORTE   = 163.42

PRODUTOS = {
    "MDA":  {"diario": "diario_mda",  "ads": "ads_mda",  "vendas": "vendas_mda"},
    "LVC":  {"diario": "diario_lvc",  "ads": "ads_lvc",  "vendas": "vendas_lvc"},
    "TEUS": {"diario": "diario_teus", "ads": "ads_teus",  "vendas": "vendas_teus"},
}

BENCH_ROAS_SAUDAVEL = 1.33
BENCH_ROAS_ALERTA   = 1.20
BENCH_ROAS_CRITICO  = 1.15

# Classificação de fases (igual ao funnel_status.py)
FASE_KEYWORDS = {
    "RMKT": ["RMKT", "REMARKETING", "[Q]", "RETARGETING"],
    "F3":   ["[F3]", "(F3)", "F3 ", "F3-"],
    "F2":   ["[F2]", "F2 ", "F2-", "ARENA", "[CBO]"],
    "F1":   ["[F1]", "(F1)", "F1 ", "F1-", "TESTE", "LAB", "1-X-1", "1-5-1", "[ABO]", "] [1]"],
    "F0":   ["F0", "ENGAJAMENTO", "AQUECIMENTO"],
}

FASE_ORDER  = {"F3": 0, "F2/F3": 1, "F2": 2, "F1": 3, "RMKT": 4, "F0": 5, "?": 6}
FASE_LABELS = {
    "F3":   "F3   -- Escala total",
    "F2/F3":"F2/F3 -- Advantage+ (escala)",
    "F2":   "F2   -- Arena VSL",
    "F1":   "F1   -- Laboratorio",
    "RMKT": "RMKT -- Remarketing",
    "F0":   "F0   -- Engajamento",
    "?":    "?    -- Nao classificado",
}
FASE_COLORS = {
    "F3": "green", "F2/F3": "green", "F2": "cyan",
    "F1": "yellow", "RMKT": "blue", "F0": "dim", "?": "dim",
}

# ── Cores no terminal ─────────────────────────────────────────────────────────
def c(text, color):
    colors = {
        "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
        "blue": "\033[94m", "cyan": "\033[96m", "bold": "\033[1m",
        "dim": "\033[2m", "reset": "\033[0m",
    }
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7
            )
        except Exception:
            pass
    return f"{colors.get(color,'')}{text}{colors['reset']}"

def roas_color(roas):
    if roas >= BENCH_ROAS_SAUDAVEL: return c(f"{roas:.2f}x", "green")
    if roas >= BENCH_ROAS_ALERTA:   return c(f"{roas:.2f}x", "yellow")
    return c(f"{roas:.2f}x", "red")

def cpa_color(cpa):
    if cpa is None: return c("sem venda", "dim")
    if cpa <= CPA_ALVO:   return c(f"R$ {cpa:.2f}", "green")
    if cpa <= CPA_BOM:    return c(f"R$ {cpa:.2f}", "green")
    if cpa <= CPA_LIMITE: return c(f"R$ {cpa:.2f}", "yellow")
    if cpa <= CPA_CORTE:  return c(f"R$ {cpa:.2f}", "yellow")
    return c(f"R$ {cpa:.2f}", "red")

def cpa_label(cpa):
    if cpa is None:       return c("[SEM VENDA]", "dim")
    if cpa <= CPA_ALVO:   return c("[ALVO-F3]", "green")
    if cpa <= CPA_BOM:    return c("[BOM-F2]", "green")
    if cpa <= CPA_LIMITE: return c("[LIMITE]", "yellow")
    if cpa <= CPA_CORTE:  return c("[CORTE]", "yellow")
    return c("[PAUSAR]", "red")

def status_icon(roas):
    if roas >= BENCH_ROAS_SAUDAVEL: return c("[OK]", "green")
    if roas >= BENCH_ROAS_ALERTA:   return c("[!!]", "yellow")
    return c("[XX]", "red")

# ── Helpers de data ───────────────────────────────────────────────────────────
def latest_sheets_date():
    """Retorna o date_label ISO mais recente (YYYY-MM-DD), ignorando aliases como 'hoje'."""
    from datetime import datetime
    files = list(SHEETS.glob("*_manifest.json"))
    if not files:
        print(c("ERRO: Nenhum dado encontrado em data/sheets/. Rode sheets_collector.py primeiro.", "red"))
        sys.exit(1)
    iso_labels = []
    for f in files:
        label = f.name.split("_")[0]
        try:
            datetime.strptime(label, "%Y-%m-%d")
            iso_labels.append(label)
        except ValueError:
            pass
    if iso_labels:
        return sorted(iso_labels)[-1]
    # fallback para qualquer label
    return sorted(f.name[:10] for f in files)[-1]

def parse_period(period, since, until):
    today = date.today()
    if since and until:
        return since, until
    if period == "today":
        return str(today), str(today)
    if period == "yesterday":
        d = today - timedelta(days=1)
        return str(d), str(d)
    if period == "week":
        start = today - timedelta(days=today.weekday())
        return str(start), str(today)
    if period == "month":
        return str(today.replace(day=1)), str(today)
    if period == "last7":
        return str(today - timedelta(days=6)), str(today)
    return str(today - timedelta(days=6)), str(today)

# ── Leitura de dados ──────────────────────────────────────────────────────────
def load_diario(produto_key, date_label, since, until):
    alias = PRODUTOS[produto_key]["diario"]
    path = SHEETS / f"{date_label}_{alias}.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)
    df = df[(df["Data"] >= since) & (df["Data"] <= until)].copy()
    # Limpar colunas monetarias
    for col in ["Gasto", "Faturamento"]:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace("R$ ", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    for col in ["Vendas", "IC", "Cliques no Link", "Alcance", "Impressoes", "VPV"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    # Alias de coluna de impressoes com acento
    if "Impressões" in df.columns:
        df["Impressões"] = pd.to_numeric(
            df["Impressões"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
            errors="coerce"
        ).fillna(0)
    return df

def load_ads(produto_key, date_label, since, until):
    alias = PRODUTOS[produto_key]["ads"]
    path = SHEETS / f"{date_label}_{alias}.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[(df["date"] >= since) & (df["date"] <= until)].copy()
    spend_col = "Spend (Cost, Amount Spent)"
    buy_col   = "Action Omni Purchase"
    imp_col   = "Impressions"
    clk_col   = "Inline Link Clicks"
    for col in [spend_col, buy_col, imp_col, clk_col]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df

def _parse_br_valor(series):
    """Converte serie de valores BR (R$ 1.234,56 ou 1234,56) para float."""
    return (
        series.astype(str)
        .str.strip()
        .str.replace(r"R\$\s*", "", regex=True)
        .str.replace("\xa0", "", regex=False)
        .str.replace(".", "", regex=False)   # remove separador de milhar
        .str.replace(",", ".", regex=False)  # virgula decimal -> ponto
        .pipe(lambda s: pd.to_numeric(s, errors="coerce").fillna(0.0))
    )

def load_vendas_raw(produto_key, date_label, since, until):
    """
    Carrega vendas_{produto}.csv sem filtro de produto principal.
    Retorna DataFrame com DATA_DT, VALOR_PAGO, PRODUTO, UTM_SOURCE, UTM_CAMPAIGN, _PRODUTO_KEY.
    Aplica apenas STATUS (APPROVED/COMPLETE) e filtro de periodo.
    Exclui acelerador automaticamente.
    """
    alias = PRODUTOS[produto_key]["vendas"]
    path = SHEETS / f"{date_label}_{alias}.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    # Data
    data_col = next(
        (c for c in df.columns if "DATA" in c.upper() or "DATE" in c.upper()),
        df.columns[0]
    )
    df["DATA_DT"] = pd.to_datetime(
        df[data_col].astype(str).str[:10].str.strip(),
        format="%d/%m/%Y", errors="coerce"
    )
    df = df[(df["DATA_DT"] >= since) & (df["DATA_DT"] <= until)].copy()

    # STATUS
    if "STATUS" in df.columns:
        df = df[df["STATUS"].isin(["APPROVED", "COMPLETE"])].copy()

    if df.empty:
        return pd.DataFrame()

    # VALOR PAGO
    valor_col = next(
        (c for c in df.columns if "VALOR" in c.upper() and "PAG" in c.upper()),
        None
    )
    df["VALOR_PAGO"] = _parse_br_valor(df[valor_col]) if valor_col else 0.0

    # UTM_SOURCE
    utm_src = next(
        (c for c in df.columns if c.upper().replace(" ", "_") == "UTM_SOURCE"),
        None
    )
    df["UTM_SOURCE"] = df[utm_src].fillna("").astype(str) if utm_src else ""

    # UTM_CAMPAIGN
    utm_camp = next(
        (c for c in df.columns if c.upper().replace(" ", "_") == "UTM_CAMPAIGN"),
        None
    )
    df["UTM_CAMPAIGN"] = df[utm_camp].fillna("").astype(str) if utm_camp else ""

    if "PRODUTO" not in df.columns:
        df["PRODUTO"] = ""

    df["_PRODUTO_KEY"] = produto_key

    return df[["DATA_DT", "VALOR_PAGO", "PRODUTO", "UTM_SOURCE", "UTM_CAMPAIGN", "_PRODUTO_KEY"]].copy()


# ── Classificação de produto principal vs orderbump ───────────────────────────

def is_produto_principal(produto_str, produto_key):
    """Retorna True se for o produto principal (nao bump)."""
    s = str(produto_str)
    if produto_key == "MDA":
        return s.startswith("Mestres do Algoritmo")
    else:  # LVC, TEUS — match exato (evita bumps com nome similar)
        return s == "Lucrando com Vídeos Curtos"

def is_acelerador(produto_str):
    return "ACELERADOR" in str(produto_str).upper()


def classify_campaign(name: str) -> str:
    name_upper = str(name).upper()
    for fase, keywords in FASE_KEYWORDS.items():
        for kw in keywords:
            if kw.upper() in name_upper:
                return fase
    if "ADV+" in name_upper or "AUTO" in name_upper:
        return "F2/F3"
    return "?"


def load_campaigns(since, until):
    """Carrega campaign_performance.csv (TIER 2) para classificacao por fase."""
    path = ROOT / "data" / "processed" / "campaign_performance.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[(df["date"] >= since) & (df["date"] <= until)].copy()
    return df[df["spend"] > 0].copy()


def load_reembolsos(date_label, since, until):
    path = SHEETS / f"{date_label}_reembolsos.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce", dayfirst=True)
    df = df[(df["DATA"] >= since) & (df["DATA"] <= until)].copy()
    df["valor_num"] = (
        df["VALOR REEMBOLSADO"].astype(str)
        .str.replace("R$ ", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df["valor_num"] = pd.to_numeric(df["valor_num"], errors="coerce").fillna(0)
    return df

# ── Calculos por produto ──────────────────────────────────────────────────────
def calc_produto(produto_key, date_label, since, until):
    df = load_diario(produto_key, date_label, since, until)
    if df.empty:
        return None
    gasto  = df["Gasto"].sum()
    vendas = int(df["Vendas"].sum())
    ic     = int(df["IC"].sum()) if "IC" in df.columns else 0
    cliques = int(df["Cliques no Link"].sum()) if "Cliques no Link" in df.columns else 0
    cpa    = round(gasto / vendas, 2) if vendas > 0 else None
    # ROAS estimado usando ticket medio (referencia visual, nao faturamento real)
    roas   = round((vendas * TICKET_MEDIO) / gasto, 2) if gasto > 0 else 0.0
    checkout = round(vendas / ic * 100, 1) if ic > 0 else 0.0
    return {
        "produto": produto_key,
        "gasto": gasto,
        "vendas": vendas,
        "ic": ic,
        "cliques": cliques,
        "cpa": cpa,
        "roas": roas,
        "checkout": checkout,
        "receita_bruta": round(vendas * TICKET_MEDIO, 2),
    }

# ── Modos de exibicao ─────────────────────────────────────────────────────────
def show_status(resultados, reembolsos_df, period_label):
    print()
    print(c("=" * 65, "bold"))
    print(c(f"  META ADS INTELLIGENCE -- STATUS", "bold") + c(f"  [{period_label}]", "cyan"))
    print(c("=" * 65, "bold"))
    print()

    total_gasto  = 0
    total_vendas = 0
    total_ic     = 0

    for r in resultados:
        if not r: continue
        total_gasto  += r["gasto"]
        total_vendas += r["vendas"]
        total_ic     += r["ic"]

        icon = status_icon(r["roas"])
        gasto_fmt = f"R$ {r['gasto']:,.2f}"
        linha = (f"  {icon}  {c(r['produto'], 'bold'):<6}  "
                 f"Gasto: {c(gasto_fmt, 'cyan')}  |  "
                 f"Vendas: {c(str(r['vendas']), 'bold')}  |  "
                 f"CPA: {cpa_color(r['cpa'])}  |  "
                 f"ROAS: {roas_color(r['roas'])}")
        print(linha)
        if r["ic"] > 0:
            chk_color = "green" if r["checkout"] >= 11 else ("yellow" if r["checkout"] >= 8 else "red")
            checkout_fmt = f"{r['checkout']}%"
            print(f"         IC: {r['ic']}  |  Checkout: {c(checkout_fmt, chk_color)}  |  "
                  f"Cliques: {r['cliques']}")
        print()

    # Reembolsos
    qtd_r  = len(reembolsos_df)
    val_r  = reembolsos_df["valor_num"].sum() if not reembolsos_df.empty else 0
    receita_bruta = total_vendas * TICKET_MEDIO
    receita_liq   = receita_bruta - val_r
    lucro         = receita_liq - total_gasto

    print(c("  " + "-" * 61, "dim"))
    print(f"  {c('TOTAL', 'bold')}        "
          f"Gasto: {c(f'R$ {total_gasto:,.2f}', 'cyan')}  |  "
          f"Vendas: {c(str(total_vendas), 'bold')}  |  "
          f"ROAS: {roas_color(round((total_vendas * TICKET_MEDIO) / total_gasto, 2) if total_gasto > 0 else 0)}")
    print()
    lucro_color = "green" if lucro > 0 else "red"
    print(f"  {'Receita estimada':<18} R$ {receita_bruta:>10,.2f}  {c('(vendas x ticket medio -- referencia)', 'dim')}")
    print(f"  {'Reembolsos':<18} {c(f'- R$ {val_r:>8,.2f}  ({qtd_r} refunds)', 'yellow')}")
    print(f"  {'Receita liquida':<18} R$ {receita_liq:>10,.2f}")
    print(f"  {'Investimento':<18} - R$ {total_gasto:>8,.2f}")
    print(f"  {c('Lucro estimado', 'bold'):<27} {c(f'R$ {lucro:>10,.2f}', lucro_color)}")
    print(c("  Use *pl para receita real (VALOR PAGO das vendas_*.csv)", "dim"))
    print()
    print(c("=" * 65, "dim"))
    print()

def show_creatives(date_label, since, until, top_n=10):
    print()
    print(c("=" * 70, "bold"))
    print(c("  RANKING DE CRIATIVOS", "bold"))
    print(c("=" * 70, "bold"))

    for produto_key in PRODUTOS:
        df = load_ads(produto_key, date_label, since, until)
        if df.empty:
            continue

        spend_col = "Spend (Cost, Amount Spent)"
        buy_col   = "Action Omni Purchase"
        clk_col   = "Inline Link Clicks"
        imp_col   = "Impressions"

        g = df.groupby("Ad Name").agg(
            gasto=(spend_col, "sum"),
            compras=(buy_col, "sum"),
            cliques=(clk_col, "sum"),
            impressoes=(imp_col, "sum"),
        ).reset_index()
        g = g[g["gasto"] > 10].copy()
        g["cpa"]  = g.apply(lambda r: round(r["gasto"] / r["compras"], 2) if r["compras"] > 0 else None, axis=1)
        g["ctr"]  = g.apply(lambda r: round(r["cliques"] / r["impressoes"] * 100, 2) if r["impressoes"] > 0 else 0, axis=1)
        g["roas"] = g.apply(lambda r: round((r["compras"] * TICKET_MEDIO) / r["gasto"], 2) if r["gasto"] > 0 else 0, axis=1)
        g = g.sort_values("gasto", ascending=False).head(top_n)

        print()
        print(f"  {c(produto_key, 'bold')} — top {min(top_n, len(g))} por gasto")
        print(c(f"  {'Ad Name':<45} {'Gasto':>8} {'Vnd':>4} {'CPA':>12} {'CTR':>6} {'Status'}", "dim"))
        print(c("  " + "-" * 85, "dim"))
        for _, r in g.iterrows():
            name = str(r["Ad Name"])[:44]
            cpa_str = f"R$ {r['cpa']:.2f}" if r["cpa"] else "sem venda"
            print(f"  {name:<45} R${r['gasto']:>7,.0f} {int(r['compras']):>4}  "
                  f"{cpa_color(r['cpa']):>12}  {r['ctr']:.2f}%  {cpa_label(r['cpa'])}")
    print()
    print(c("=" * 70, "dim"))
    print()

def show_alerts(resultados, date_label, since, until):
    print()
    print(c("=" * 65, "bold"))
    print(c("  ALERTAS -- ACOES URGENTES", "bold"))
    print(c("=" * 65, "bold"))
    print()

    alertas = []

    for r in resultados:
        if not r: continue
        cpa = r["cpa"]
        if cpa and cpa > CPA_CORTE:
            alertas.append((1, r["produto"], f"CPA R$ {cpa:.2f} -- acima do CORTE (R$ {CPA_CORTE})", "red"))
        elif r["roas"] > 0 and r["roas"] < BENCH_ROAS_ALERTA:
            alertas.append((2, r["produto"], f"ROAS {r['roas']:.2f}x -- abaixo do benchmark ({BENCH_ROAS_ALERTA}x)", "yellow"))
        if r["checkout"] > 0 and r["checkout"] < 8:
            alertas.append((1, r["produto"], f"Checkout {r['checkout']}% -- critico (< 8%)", "red"))

    # Criativos urgentes
    for produto_key in PRODUTOS:
        df = load_ads(produto_key, date_label, since, until)
        if df.empty:
            continue
        spend_col = "Spend (Cost, Amount Spent)"
        buy_col   = "Action Omni Purchase"
        g = df.groupby("Ad Name").agg(
            gasto=(spend_col, "sum"),
            compras=(buy_col, "sum"),
        ).reset_index()
        g = g[g["gasto"] > 50].copy()
        g["cpa"] = g.apply(lambda r: round(r["gasto"] / r["compras"], 2) if r["compras"] > 0 else None, axis=1)
        urgentes = g[(g["cpa"].notna()) & (g["cpa"] > CPA_CORTE)].sort_values("cpa", ascending=False)
        sem_venda = g[(g["cpa"].isna()) & (g["gasto"] > TICKET_MEDIO)]
        for _, row in urgentes.head(5).iterrows():
            name = str(row["Ad Name"])[:50]
            alertas.append((1, produto_key, f"PAUSAR {name} -- CPA R$ {row['cpa']:.2f}", "red"))
        for _, row in sem_venda.head(3).iterrows():
            name = str(row["Ad Name"])[:50]
            alertas.append((2, produto_key, f"SEM VENDA -- {name} -- R$ {row['gasto']:.0f} gastos", "yellow"))

    if not alertas:
        print(c("  Nenhum alerta critico no periodo.", "green"))
    else:
        for prio, produto, msg, color in sorted(alertas, key=lambda x: x[0]):
            icon = c("[XX]", "red") if prio == 1 else c("[!!]", "yellow")
            print(f"  {icon} [{c(produto, 'bold')}] {c(msg, color)}")
    print()
    print(c("=" * 65, "dim"))
    print()


def show_pl(resultados, reembolsos_df, period_label, date_label, since, until):
    """
    P&L com receita REAL (VALOR PAGO das vendas_*.csv).
    Separa produto principal vs order bumps.
    Inclui reembolsos discriminados por produto.
    """
    print()
    print(c("=" * 70, "bold"))
    print(c(f"  P&L DETALHADO -- {period_label}", "bold"))
    print(c("=" * 70, "bold"))
    print()

    # Carregar vendas reais (todas, sem filtro de produto principal)
    all_vendas = []
    for pk in PRODUTOS:
        df = load_vendas_raw(pk, date_label, since, until)
        if not df.empty:
            all_vendas.append(df)

    vendas_df = pd.concat(all_vendas, ignore_index=True) if all_vendas else pd.DataFrame()

    if not vendas_df.empty:
        vendas_df["_tipo"] = vendas_df.apply(
            lambda row: "acelerador" if is_acelerador(row["PRODUTO"])
            else ("principal" if is_produto_principal(row["PRODUTO"], row["_PRODUTO_KEY"])
                  else "bump"),
            axis=1
        )
        vendas_df = vendas_df[vendas_df["_tipo"] != "acelerador"].copy()

    total_gasto     = 0
    total_principal = 0.0
    total_bumps     = 0.0

    print(c(f"  {'Prod':<4}  {'Gasto':>11}  {'Principal':>11}  {'Bumps':>10}  {'Total':>11}  {'Lucro':>11}", "dim"))
    print(c("  " + "-" * 63, "dim"))

    for r in resultados:
        if not r:
            continue
        pk    = r["produto"]
        gasto = r["gasto"]
        total_gasto += gasto

        if not vendas_df.empty:
            prod_v = vendas_df[vendas_df["_PRODUTO_KEY"] == pk]
            rec_p  = prod_v[prod_v["_tipo"] == "principal"]["VALOR_PAGO"].sum()
            rec_b  = prod_v[prod_v["_tipo"] == "bump"]["VALOR_PAGO"].sum()
        else:
            rec_p = rec_b = 0.0

        total_principal += rec_p
        total_bumps     += rec_b
        rec_tot  = rec_p + rec_b
        lucro    = rec_tot - gasto
        lc       = "green" if lucro >= 0 else "red"

        print(f"  {c(pk, 'bold'):<4}  "
              f"R$ {gasto:>9,.2f}  "
              f"R$ {rec_p:>9,.2f}  "
              f"R$ {rec_b:>8,.2f}  "
              f"R$ {rec_tot:>9,.2f}  "
              f"{c(f'R$ {lucro:>9,.2f}', lc)}")

    # Detalhamento dos bumps
    if not vendas_df.empty:
        bumps_df = vendas_df[vendas_df["_tipo"] == "bump"]
        if not bumps_df.empty:
            print()
            print(c("  Order Bumps (detalhamento):", "dim"))
            by_bump = (bumps_df.groupby("PRODUTO")
                       .agg(qtd=("VALOR_PAGO", "count"), valor=("VALOR_PAGO", "sum"))
                       .sort_values("valor", ascending=False))
            for prod, row in by_bump.head(8).iterrows():
                print(f"    {str(prod)[:48]:<48}  {int(row['qtd']):>3}x  R$ {row['valor']:>8,.2f}")

    # Reembolsos por produto
    total_reembolsos = 0.0
    if not reembolsos_df.empty:
        print()
        print(c("  Reembolsos (detalhamento):", "dim"))
        by_prod = reembolsos_df.groupby("PRODUTO").agg(
            qtd=("valor_num", "count"),
            valor=("valor_num", "sum")
        ).sort_values("valor", ascending=False)
        for prod, row in by_prod.iterrows():
            print(f"    {str(prod)[:48]:<48}  {int(row['qtd']):>3}x  R$ {row['valor']:>8,.2f}")
        total_reembolsos = reembolsos_df["valor_num"].sum()

    total_bruto = total_principal + total_bumps
    receita_liq = total_bruto - total_reembolsos
    lucro_liq   = receita_liq - total_gasto
    lc          = "green" if lucro_liq >= 0 else "red"
    margem      = lucro_liq / total_gasto * 100 if total_gasto > 0 else 0
    bump_pct    = total_bumps / total_bruto * 100 if total_bruto > 0 else 0

    print()
    print(c("  " + "-" * 63, "dim"))
    print(f"  {'Receita principal':<22} R$ {total_principal:>10,.2f}")
    print(f"  {'Receita bumps':<22} R$ {total_bumps:>10,.2f}  {c(f'({bump_pct:.1f}% do bruto)', 'dim')}")
    print(f"  {'Receita bruta real':<22} R$ {total_bruto:>10,.2f}")
    print(f"  {'Reembolsos':<22} {c(f'- R$ {total_reembolsos:>8,.2f}', 'yellow')}  ({len(reembolsos_df)} refunds)")
    print(f"  {'Receita liquida':<22} R$ {receita_liq:>10,.2f}")
    print(f"  {'Investimento Meta':<22} - R$ {total_gasto:>8,.2f}")
    print(f"  {c('LUCRO LIQUIDO', 'bold'):<31} {c(f'R$ {lucro_liq:>10,.2f}', lc)}")
    print(f"  {'Margem s/ gasto':<22} {c(f'{margem:.1f}%', lc)}")
    print()
    print(c("=" * 70, "dim"))
    print()


def show_budget_distribution(since, until, period_label):
    print()
    print(c("=" * 65, "bold"))
    print(c("  DISTRIBUICAO DE ORCAMENTO POR FASE", "bold") + c(f"  [{period_label}]", "cyan"))
    print(c("=" * 65, "bold"))
    print()

    camps = load_campaigns(since, until)
    if camps.empty:
        print(c("  Sem dados de campanha (campaign_performance.csv nao encontrado).", "yellow"))
        print(c("  Rode: python scripts/data_processor.py", "dim"))
        print()
        print(c("=" * 65, "dim"))
        print()
        return

    # Agrupa por campanha e classifica fase
    g = camps.groupby("campaign_name").agg(gasto=("spend", "sum")).reset_index()
    g["fase"] = g["campaign_name"].apply(classify_campaign)

    # Agrega por fase
    por_fase = g.groupby("fase").agg(
        gasto=("gasto", "sum"),
        campanhas=("campaign_name", "count"),
    ).reset_index()

    total = por_fase["gasto"].sum()
    if total == 0:
        print(c("  Sem gasto no periodo.", "dim"))
        print()
        return

    por_fase["pct"] = por_fase["gasto"] / total * 100
    por_fase["_ord"] = por_fase["fase"].map(lambda x: FASE_ORDER.get(x, 9))
    por_fase = por_fase.sort_values("_ord").drop(columns="_ord")

    print(c(f"  {'Fase':<26} {'Gasto':>12}  {'% Total':>9}  {'Camps':>5}", "dim"))
    print(c("  " + "-" * 59, "dim"))

    for _, r in por_fase.iterrows():
        fase   = r["fase"]
        label  = FASE_LABELS.get(fase, fase)
        color  = FASE_COLORS.get(fase, "reset")
        bar_n  = max(1, int(r["pct"] / 5))
        bar    = "#" * bar_n + "." * (20 - bar_n)
        pct_str = f"{r['pct']:.1f}%"
        gasto_str = f"R$ {r['gasto']:>9,.0f}"
        print(f"  {c(label, color):<36}  {gasto_str}  {c(pct_str, color):>13}  {int(r['campanhas']):>5}")

    print(c("  " + "-" * 59, "dim"))
    print(f"  {'TOTAL':<26}  R$ {total:>9,.0f}  {'100.0%':>9}")
    print()
    print(c("  Referencia ideal:", "dim"))
    print(c("  F1: 10-15%  |  F2: 30-40%  |  F3: 40-50%  |  RMKT: 5-10%", "dim"))
    print()
    print(c("=" * 65, "dim"))
    print()


def show_vendas_origem(date_label, since, until, period_label):
    """
    Agrupa vendas reais por canal de origem (UTM_SOURCE).
    Mostra: Origem | Qtd Vendas | Receita | % Total.
    """
    print()
    print(c("=" * 65, "bold"))
    print(c(f"  VENDAS POR ORIGEM -- {period_label}", "bold"))
    print(c("=" * 65, "bold"))
    print()

    all_vendas = []
    for pk in PRODUTOS:
        df = load_vendas_raw(pk, date_label, since, until)
        if not df.empty:
            all_vendas.append(df)

    if not all_vendas:
        print(c("  Sem dados de vendas no periodo.", "yellow"))
        print(c("=" * 65, "dim"))
        print()
        return

    vendas_df = pd.concat(all_vendas, ignore_index=True)
    # Excluir acelerador
    vendas_df = vendas_df[~vendas_df["PRODUTO"].apply(is_acelerador)].copy()

    # Normalizar UTM_SOURCE para nomes legíveis
    def _normalizar_origem(raw):
        s = str(raw).strip().lower()
        if s in ("", "nan", "none", "direct", "organico", "organica", "organic"):
            return "Direto / Organico"
        if "facebook" in s or s == "fb":
            return "Facebook"
        if "instagram" in s:
            return "Instagram"
        if "bio" in s or "linktree" in s:
            return "Bio / Link"
        if "hotmart" in s:
            return "Hotmart"
        if "manychat" in s or "many" in s:
            return "Manychat"
        if "comercial" in s:
            return "Comercial"
        if "youtube" in s or "yt" == s:
            return "YouTube"
        return s.title()

    vendas_df["ORIGEM"] = vendas_df["UTM_SOURCE"].apply(_normalizar_origem)

    total_receita = vendas_df["VALOR_PAGO"].sum()
    total_qtd     = len(vendas_df)

    if total_qtd == 0:
        print(c("  Nenhuma venda no periodo.", "dim"))
        print(c("=" * 65, "dim"))
        print()
        return

    by_origem = (
        vendas_df.groupby("ORIGEM")
        .agg(qtd=("VALOR_PAGO", "count"), receita=("VALOR_PAGO", "sum"))
        .sort_values("receita", ascending=False)
    )

    print(c(f"  {'Origem':<22}  {'Vendas':>7}  {'% Qtd':>6}  {'Receita':>12}  {'% Receita':>10}", "dim"))
    print(c("  " + "-" * 63, "dim"))

    for origem, row in by_origem.iterrows():
        pct_qtd = row["qtd"] / total_qtd * 100
        pct_rec = row["receita"] / total_receita * 100
        orig_str = str(origem)[:21]
        print(f"  {orig_str:<22}  {int(row['qtd']):>7}  {pct_qtd:>5.1f}%  "
              f"R$ {row['receita']:>9,.2f}  {pct_rec:>9.1f}%")

    print(c("  " + "-" * 63, "dim"))
    print(f"  {'TOTAL':<22}  {total_qtd:>7}  {'100%':>6}  R$ {total_receita:>9,.2f}  {'100%':>10}")

    # Alertas: se "Direto/Organico" > 40% = muita venda sem tracking UTM
    direto_pct = 0
    if "Direto / Organico" in by_origem.index:
        direto_pct = by_origem.loc["Direto / Organico", "qtd"] / total_qtd * 100
    if direto_pct > 10:
        print()
        print(c(f"  [!!] {direto_pct:.0f}% das vendas sem UTM -- tracking pode estar incompleto", "yellow"))

    print()
    print(c("=" * 65, "dim"))
    print()


def show_funil_checkout(date_label, since, until, period_label):
    """
    Funil de checkout por produto: Impressoes -> Cliques -> VPV -> IC -> Vendas.
    Calcula taxas de conversao em cada etapa e emite alertas.
    Nota: Vendas = pixel Meta (pode subestimar) -- usar *pl para faturamento real.
    """
    print()
    print(c("=" * 70, "bold"))
    print(c(f"  FUNIL DE CHECKOUT -- {period_label}", "bold"))
    print(c("=" * 70, "bold"))
    print()

    total_impressoes = 0.0
    total_cliques    = 0.0
    total_vpv        = 0.0
    total_ic         = 0.0
    total_vendas     = 0.0

    print(c(f"  {'Prod':<4}  {'VPV':>8}  {'IC':>8}  {'Vendas':>7}  {'VPV->IC':>8}  {'IC->Venda':>10}  {'VPV->Venda':>11}", "dim"))
    print(c("  " + "-" * 63, "dim"))

    for pk in PRODUTOS:
        df = load_diario(pk, date_label, since, until)
        if df.empty:
            continue

        # Impressoes (aceita coluna com ou sem acento)
        impressoes = 0.0
        if "Impressões" in df.columns:
            impressoes = float(df["Impressões"].sum())
        elif "Impressoes" in df.columns:
            impressoes = float(df["Impressoes"].sum())

        cliques = float(df["Cliques no Link"].sum()) if "Cliques no Link" in df.columns else 0.0
        vpv     = float(df["VPV"].sum()) if "VPV" in df.columns else 0.0
        ic      = float(df["IC"].sum()) if "IC" in df.columns else 0.0
        vendas  = float(df["Vendas"].sum()) if "Vendas" in df.columns else 0.0

        total_impressoes += impressoes
        total_cliques    += cliques
        total_vpv        += vpv
        total_ic         += ic
        total_vendas     += vendas

        # Taxas
        vpv_ic_rate    = ic / vpv * 100 if vpv > 0 else 0.0
        ic_venda_rate  = vendas / ic * 100 if ic > 0 else 0.0
        vpv_venda_rate = vendas / vpv * 100 if vpv > 0 else 0.0

        vpv_ic_clr    = "green" if vpv_ic_rate >= 25 else ("yellow" if vpv_ic_rate >= 15 else "red")
        ic_vnd_clr    = "green" if ic_venda_rate >= 11 else ("yellow" if ic_venda_rate >= 8 else "red")
        vpv_vnd_clr   = "green" if vpv_venda_rate >= 3 else ("yellow" if vpv_venda_rate >= 2 else "red")

        # Linha sem ANSI nos campos numéricos para manter alinhamento
        print(f"  {c(pk, 'bold'):<4}  "
              f"{int(vpv):>8,}  {int(ic):>8,}  {int(vendas):>7,}  "
              f"{c(f'{vpv_ic_rate:.1f}%', vpv_ic_clr):<20}"
              f"{c(f'{ic_venda_rate:.1f}%', ic_vnd_clr):<21}"
              f"{c(f'{vpv_venda_rate:.1f}%', vpv_vnd_clr)}")

    # Totais
    print(c("  " + "-" * 63, "dim"))
    vpv_ic_total    = total_ic / total_vpv * 100 if total_vpv > 0 else 0.0
    ic_venda_total  = total_vendas / total_ic * 100 if total_ic > 0 else 0.0
    vpv_venda_total = total_vendas / total_vpv * 100 if total_vpv > 0 else 0.0
    clk_vpv_total   = total_vpv / total_cliques * 100 if total_cliques > 0 else 0.0
    ctr_total       = total_cliques / total_impressoes * 100 if total_impressoes > 0 else 0.0

    vpv_ic_clr   = "green" if vpv_ic_total >= 25 else ("yellow" if vpv_ic_total >= 15 else "red")
    ic_vnd_clr   = "green" if ic_venda_total >= 11 else ("yellow" if ic_venda_total >= 8 else "red")
    vpv_vnd_clr  = "green" if vpv_venda_total >= 3 else ("yellow" if vpv_venda_total >= 2 else "red")

    print(f"  {'TOTAL':<4}  "
          f"{int(total_vpv):>8,}  {int(total_ic):>8,}  {int(total_vendas):>7,}  "
          f"{c(f'{vpv_ic_total:.1f}%', vpv_ic_clr):<20}"
          f"{c(f'{ic_venda_total:.1f}%', ic_vnd_clr):<21}"
          f"{c(f'{vpv_venda_total:.1f}%', vpv_vnd_clr)}")

    # Funil completo (texto)
    print()
    print(c("  Funil consolidado:", "dim"))
    if total_impressoes > 0:
        print(f"  Impressoes {int(total_impressoes):,}  ->  Cliques {int(total_cliques):,}  (CTR {ctr_total:.2f}%)")
    if total_cliques > 0:
        print(f"  Cliques {int(total_cliques):,}  ->  VPV {int(total_vpv):,}  ({clk_vpv_total:.1f}% page-view rate)")
    if total_vpv > 0:
        print(f"  VPV {int(total_vpv):,}  ->  IC {int(total_ic):,}  "
              f"({c(f'{vpv_ic_total:.1f}%', vpv_ic_clr)} iniciaram checkout)")
    if total_ic > 0:
        print(f"  IC {int(total_ic):,}  ->  Vendas {int(total_vendas):,}  "
              f"({c(f'{ic_venda_total:.1f}%', ic_vnd_clr)} taxa de checkout)")

    # Alertas automaticos
    alertas = []
    if ic_venda_total > 0 and ic_venda_total < 8:
        alertas.append(c(f"  [XX] IC->Venda {ic_venda_total:.1f}% -- critico (meta >= 11%, minimo >= 8%)", "red"))
    elif ic_venda_total > 0 and ic_venda_total < 11:
        alertas.append(c(f"  [!!] IC->Venda {ic_venda_total:.1f}% -- abaixo do alvo (>= 11%)", "yellow"))
    if vpv_ic_total > 0 and vpv_ic_total < 15:
        alertas.append(c(f"  [!!] VPV->IC {vpv_ic_total:.1f}% -- fraco -- verificar copy/oferta da pagina de vendas", "yellow"))

    if alertas:
        print()
        print(c("  Alertas:", "bold"))
        for a in alertas:
            print(a)

    print()
    print(c("  Benchmarks: IC->Venda >= 11% bom | >= 8% ok | < 8% critico", "dim"))
    print(c("  VPV->IC >= 25% bom | >= 15% ok | < 15% revisar pagina", "dim"))
    print(c("  Nota: Vendas = pixel Meta (pode subestimar real) -- usar *pl para faturamento", "dim"))
    print()
    print(c("=" * 70, "dim"))
    print()


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Meta Ads -- Quick Status")
    parser.add_argument("--period", default="week",
                        choices=["today", "yesterday", "week", "month", "last7"],
                        help="Periodo de analise")
    parser.add_argument("--since", help="Data inicio YYYY-MM-DD")
    parser.add_argument("--until", help="Data fim YYYY-MM-DD")
    parser.add_argument("--mode", default="status",
                        choices=["status", "creatives", "alerts", "pl", "budget",
                                 "origem", "checkout", "all"],
                        help="Modo de exibicao")
    args = parser.parse_args()

    since_str, until_str = parse_period(args.period, args.since, args.until)
    since = pd.Timestamp(since_str)
    until = pd.Timestamp(until_str)
    period_label = f"{since_str} a {until_str}"

    mode = args.mode

    # budget nao depende de data/sheets
    if mode == "budget":
        show_budget_distribution(since, until, period_label)
        return

    date_label = latest_sheets_date()
    resultados   = [calc_produto(k, date_label, since, until) for k in PRODUTOS]
    reembolsos   = load_reembolsos(date_label, since, until)

    if mode in ("status", "all"):
        show_status(resultados, reembolsos, period_label)
    if mode in ("creatives", "all"):
        show_creatives(date_label, since, until)
    if mode in ("alerts", "all"):
        show_alerts(resultados, date_label, since, until)
    if mode in ("pl", "all"):
        show_pl(resultados, reembolsos, period_label, date_label, since, until)
    if mode in ("origem", "all"):
        show_vendas_origem(date_label, since, until, period_label)
    if mode in ("checkout", "all"):
        show_funil_checkout(date_label, since, until, period_label)
    if mode == "all":
        show_budget_distribution(since, until, period_label)


if __name__ == "__main__":
    main()
