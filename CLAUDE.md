# Meta Ads Intelligence — Claude Code Configuration

## Project Purpose

Read-only Meta Marketing API intelligence system. Collects ad account data, processes it into CSVs, analyzes performance with @analyst, and generates structured reports.

**Phase: Read-Only** — No writes to Meta API. All actions are local. User reviews all recommendations before acting.

---

## Key Paths

| Path | Description |
|------|-------------|
| `scripts/meta_collector.py` | Fetches raw data from Meta API → `data/raw/` |
| `scripts/data_processor.py` | Normalizes JSONs → CSVs in `data/processed/` |
| `config/analyst-rules.md` | User-defined analysis rules (read first, always) |
| `data/raw/` | Raw JSON from API — gitignored, immutable after fetch |
| `data/processed/` | Normalized CSVs — source of truth for analysis |
| `docs/reports/` | Generated Markdown reports |
| `.ai/` | Analysis JSON artifacts — gitignored |
| `templates/` | Report templates |
| `.aios-core/development/` | AIOS tasks and workflow definitions |

---

## Default Agent

**@analyst** — Primary agent for analysis and report generation.

For data collection tasks, use **@dev**.

---

## Workflow

```
*workflow meta-ads-intelligence
```

Steps:
1. **fetch-meta-data** (@dev) — Runs `meta_collector.py` + `data_processor.py`
2. **analyze-meta-performance** (@analyst) — Reads CSVs, applies analyst-rules.md, produces JSON artifact
3. **generate-meta-report** (@analyst) — Renders Markdown report from JSON artifact

---

## Critical Rules

### data/raw/ is Immutable
- Never edit raw JSON files manually
- Re-run `meta_collector.py` to refresh
- Raw files are gitignored — do not commit

### analyst-rules.md is Always Read First
- Every analysis MUST read `config/analyst-rules.md` before applying defaults
- User rules override all built-in thresholds
- Field `rules_applied` in the JSON artifact must list which rules were used

### Idempotency
- All scripts can be re-run for the same date without duplicating data
- Existing files are overwritten, not appended

### Read-Only Phase
- No modifications to Meta API (no budget changes, no pause/start, no edits)
- Scripts only perform GET requests
- All recommendations are for user review only

---

## Setup (once)

```bash
# 1. Copy credentials
cp .env.example .env
# Edit .env with your Meta API credentials

# 2. Install dependencies
pip install -r scripts/requirements.txt

# 3. Run pipeline
python scripts/meta_collector.py --date-range yesterday
python scripts/data_processor.py --date $(date +%Y-%m-%d)
```

---

## Meta API Permissions Required

- `ads_read`
- `read_insights`
- `business_management`

---

*Synkra AIOS — Meta Ads Intelligence v1.0*
