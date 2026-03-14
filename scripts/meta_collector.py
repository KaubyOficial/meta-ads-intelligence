#!/usr/bin/env python3
"""
Meta Ads Intelligence — Data Collector
Fetches campaigns, ad sets, ads, and insights from Meta Marketing API.
Saves raw JSON to data/raw/ and writes a manifest file.

Usage:
    python scripts/meta_collector.py --date-range yesterday
    python scripts/meta_collector.py --date-range last_7d --account-id act_XXXX

Date ranges: today | yesterday | last_7d | last_30d
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

# ── Load .env from project root ───────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ── Lazy import Facebook SDK (fail loudly with install hint) ──────────────────
try:
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.ad import Ad
    from facebook_business.exceptions import FacebookRequestError
except ImportError:
    print("ERROR: facebook-business SDK not installed.")
    print("Run: pip install -r scripts/requirements.txt")
    sys.exit(1)


# ── Constants ─────────────────────────────────────────────────────────────────
CAMPAIGN_FIELDS = [
    "id", "name", "status", "objective",
    "daily_budget", "lifetime_budget",
    "start_time", "stop_time", "created_time", "updated_time",
]

ADSET_FIELDS = [
    "id", "name", "campaign_id", "status",
    "daily_budget", "lifetime_budget",
    "bid_amount", "bid_strategy", "optimization_goal",
    "targeting", "start_time", "end_time", "created_time",
]

AD_FIELDS = [
    "id", "name", "adset_id", "campaign_id",
    "status", "creative", "created_time", "updated_time",
]

INSIGHT_FIELDS = [
    "impressions", "reach", "clicks", "spend",
    "cpc", "ctr", "cpm", "frequency",
    "actions", "action_values",
    "campaign_id", "campaign_name",
    "adset_id", "adset_name",
    "ad_id", "ad_name",
    "date_start", "date_stop",
]


# ── Date range helpers ────────────────────────────────────────────────────────
def resolve_date_range(date_range: str) -> tuple[str, str]:
    today = date.today()
    if date_range == "today":
        return str(today), str(today)
    elif date_range == "yesterday":
        d = today - timedelta(days=1)
        return str(d), str(d)
    elif date_range == "last_7d":
        return str(today - timedelta(days=7)), str(today - timedelta(days=1))
    elif date_range == "last_30d":
        return str(today - timedelta(days=30)), str(today - timedelta(days=1))
    else:
        raise ValueError(f"Unknown date_range: {date_range}. Choose: today | yesterday | last_7d | last_30d")


# ── Pagination helper ─────────────────────────────────────────────────────────
def fetch_cursor_pages(cursor, max_retries: int = 5) -> list[dict]:
    """Iterate a cursor that supports direct iteration and has_next_page."""
    results = []
    attempt = 0
    page = cursor
    while True:
        try:
            for item in page:
                results.append(item.export_all_data())
            # The Meta SDK modifies `page` in-place via load_next_page().
            # Returns False when there are no more pages.
            if not page.load_next_page():
                break
            # Reset attempt counter after successful page
            attempt = 0
        except StopIteration:
            break
        except FacebookRequestError as e:
            error_code = e.api_error_code()
            if error_code == 80000:
                wait = 2 ** attempt
                attempt += 1
                if attempt > max_retries:
                    raise
                print(f"  Rate limit. Waiting {wait}s...")
                time.sleep(wait)
            elif error_code in (190, 102, 2500):
                print(f"\nERROR: Invalid/expired token (code {error_code}). Update META_ACCESS_TOKEN in .env")
                sys.exit(1)
            else:
                raise
        except Exception:
            break
    return results


# ── JSON serializer ───────────────────────────────────────────────────────────
def _json_serializer(obj):
    """Serialize datetime objects preserving timezone via isoformat."""
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    return str(obj)


# ── Main collector ────────────────────────────────────────────────────────────
def collect(account_id: str, date_since: str, date_until: str, raw_dir: Path) -> dict:
    print(f"\n{'='*60}")
    print(f"Meta Ads Collector — {date_since} to {date_until}")
    print(f"Account: {account_id}")
    print(f"{'='*60}\n")

    account = AdAccount(account_id)

    manifest = {
        "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "account_id": account_id,
        "date_since": date_since,
        "date_until": date_until,
        "counts": {},
        "files": {},
        "warnings": [],
    }

    # Use date_since as the primary date label for filenames
    date_label = date_since

    # ── 1. Campaigns ──────────────────────────────────────────────────────────
    print("Fetching campaigns...")
    try:
        campaigns_cursor = account.get_campaigns(fields=CAMPAIGN_FIELDS)
        campaigns = fetch_cursor_pages(campaigns_cursor)
    except Exception as e:
        print(f"  WARNING: Could not fetch campaigns: {e}")
        campaigns = []
        manifest["warnings"].append(f"campaigns: {str(e)}")

    campaigns_file = raw_dir / "campaigns" / f"{date_label}_campaigns.json"
    campaigns_file.parent.mkdir(parents=True, exist_ok=True)
    campaigns_file.write_text(json.dumps(campaigns, indent=2, default=_json_serializer), encoding="utf-8")
    manifest["counts"]["campaigns"] = len(campaigns)
    manifest["files"]["campaigns"] = str(campaigns_file.relative_to(PROJECT_ROOT))
    print(f"  → {len(campaigns)} campaigns saved")

    # ── 2. Ad Sets ────────────────────────────────────────────────────────────
    print("Fetching ad sets...")
    try:
        adsets_cursor = account.get_ad_sets(fields=ADSET_FIELDS)
        adsets = fetch_cursor_pages(adsets_cursor)
    except Exception as e:
        print(f"  WARNING: Could not fetch ad sets: {e}")
        adsets = []
        manifest["warnings"].append(f"adsets: {str(e)}")

    adsets_file = raw_dir / "adsets" / f"{date_label}_adsets.json"
    adsets_file.parent.mkdir(parents=True, exist_ok=True)
    adsets_file.write_text(json.dumps(adsets, indent=2, default=_json_serializer), encoding="utf-8")
    manifest["counts"]["adsets"] = len(adsets)
    manifest["files"]["adsets"] = str(adsets_file.relative_to(PROJECT_ROOT))
    print(f"  → {len(adsets)} ad sets saved")

    # ── 3. Ads ────────────────────────────────────────────────────────────────
    print("Fetching ads...")
    try:
        ads_cursor = account.get_ads(fields=AD_FIELDS)
        ads = fetch_cursor_pages(ads_cursor)
    except Exception as e:
        print(f"  WARNING: Could not fetch ads: {e}")
        ads = []
        manifest["warnings"].append(f"ads: {str(e)}")

    ads_file = raw_dir / "ads" / f"{date_label}_ads.json"
    ads_file.parent.mkdir(parents=True, exist_ok=True)
    ads_file.write_text(json.dumps(ads, indent=2, default=_json_serializer), encoding="utf-8")
    manifest["counts"]["ads"] = len(ads)
    manifest["files"]["ads"] = str(ads_file.relative_to(PROJECT_ROOT))
    print(f"  → {len(ads)} ads saved")

    # ── 4. Insights ───────────────────────────────────────────────────────────
    print("Fetching insights...")
    days_span = (date.fromisoformat(date_until) - date.fromisoformat(date_since)).days + 1
    if days_span <= 7:
        time_increment = 1
    else:
        time_increment = 7  # Weekly aggregation for ranges > 7 days
    params = {
        "time_range": {"since": date_since, "until": date_until},
        "level": "ad",
        "time_increment": time_increment,
    }
    try:
        insights_cursor = account.get_insights(fields=INSIGHT_FIELDS, params=params)
        insights = fetch_cursor_pages(insights_cursor)
    except Exception as e:
        print(f"  WARNING: Could not fetch insights: {e}")
        insights = []
        manifest["warnings"].append(f"insights: {str(e)}")

    insights_file = raw_dir / "insights" / f"{date_label}_insights.json"
    insights_file.parent.mkdir(parents=True, exist_ok=True)
    insights_file.write_text(json.dumps(insights, indent=2, default=_json_serializer), encoding="utf-8")
    manifest["counts"]["insights_rows"] = len(insights)
    manifest["files"]["insights"] = str(insights_file.relative_to(PROJECT_ROOT))
    print(f"  → {len(insights)} insight rows saved")

    # ── Manifest ──────────────────────────────────────────────────────────────
    manifest_file = raw_dir / f"{date_label}_manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2, default=_json_serializer), encoding="utf-8")

    empty_entities = []
    if not campaigns:
        empty_entities.append("campaigns")
    if not adsets:
        empty_entities.append("adsets")
    if not ads:
        empty_entities.append("ads")
    if not insights:
        empty_entities.append("insights")

    if empty_entities:
        if len(empty_entities) == 4:
            manifest["warnings"].append("No data collected — check account ID and token permissions")
        else:
            manifest["warnings"].append(f"Partial data: empty entities: {', '.join(empty_entities)}")

    print(f"\n{'='*60}")
    print("Collection complete!")
    print(f"  Campaigns:    {manifest['counts'].get('campaigns', 0)}")
    print(f"  Ad Sets:      {manifest['counts'].get('adsets', 0)}")
    print(f"  Ads:          {manifest['counts'].get('ads', 0)}")
    print(f"  Insight rows: {manifest['counts'].get('insights_rows', 0)}")
    if manifest["warnings"]:
        print(f"\nWarnings:")
        for w in manifest["warnings"]:
            print(f"  ⚠ {w}")
    print(f"\nManifest: {manifest_file}")
    print(f"{'='*60}\n")

    return manifest


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Meta Ads Intelligence — Data Collector")
    parser.add_argument(
        "--date-range",
        choices=["today", "yesterday", "last_7d", "last_30d"],
        default="yesterday",
        help="Date range to collect (default: yesterday)",
    )
    parser.add_argument(
        "--account-id",
        default=None,
        help="Ad account ID (e.g., act_123456). Defaults to META_AD_ACCOUNT_ID in .env",
    )
    args = parser.parse_args()

    # ── Credentials ───────────────────────────────────────────────────────────
    access_token = os.getenv("META_ACCESS_TOKEN")
    account_id = args.account_id or os.getenv("META_AD_ACCOUNT_ID")
    app_id = os.getenv("META_APP_ID")
    app_secret = os.getenv("META_APP_SECRET")
    api_version = os.getenv("META_API_VERSION", "v19.0")

    if not access_token:
        print("ERROR: META_ACCESS_TOKEN not set. Create a .env file from .env.example")
        sys.exit(1)
    if not account_id:
        print("ERROR: META_AD_ACCOUNT_ID not set and --account-id not provided")
        sys.exit(1)
    if not account_id.startswith("act_"):
        account_id = f"act_{account_id}"

    if not re.match(r'^act_\d+$', account_id):
        print(f"ERROR: Invalid account ID format: '{account_id}'. Expected: act_XXXXXXX (digits only)")
        sys.exit(1)

    # ── Initialize API ────────────────────────────────────────────────────────
    if not app_id or not app_secret:
        print("WARNING: META_APP_ID and/or META_APP_SECRET not set in .env")
        print("  Some API calls may fail. See .env.example for required variables.")

    FacebookAdsApi.init(
        app_id=app_id or "0",
        app_secret=app_secret or "",
        access_token=access_token,
        api_version=api_version,
    )

    date_since, date_until = resolve_date_range(args.date_range)
    raw_dir = PROJECT_ROOT / "data" / "raw"

    collect(account_id, date_since, date_until, raw_dir)


if __name__ == "__main__":
    main()
