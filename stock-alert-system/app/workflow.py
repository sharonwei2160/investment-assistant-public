import os
import json
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo

from stock_service import get_stock_prices
from aws_service import save_stock_price
from line_service import (
    send_stock_alert,
    send_fetch_failed_alert,
    send_workflow_failed_alert
)


def load_watchlist(target_market=None):
    with open("app/watchlist.json", "r", encoding="utf-8") as file:
        watchlist = json.load(file)

    if target_market:
        watchlist = [
            stock for stock in watchlist
            if stock.get("market") == target_market
        ]

    return watchlist


def write_github_summary(
    market_name,
    total_count,
    success_count,
    failed_count,
    alert_count,
    line_sent
):
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")

    if not summary_path:
        return

    now_tw = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")

    summary = f"""
# Stock Alert Health Check

| Item | Value |
|---|---|
| Run Time (Taipei) | {now_tw} |
| Market | {market_name} |
| Total Stocks | {total_count} |
| Success Stocks | {success_count} |
| Failed Stocks | {failed_count} |
| Alert Stocks | {alert_count} |
| LINE Alert Sent | {"Yes" if line_sent else "No"} |
"""

    with open(summary_path, "a", encoding="utf-8") as file:
        file.write(summary)


def run_workflow(target_market=None):
    market_name = target_market if target_market else "ALL"

    watchlist = load_watchlist(target_market)

    prices, failed_stocks = get_stock_prices(watchlist)

    if failed_stocks:
        send_fetch_failed_alert(failed_stocks, market_name)

    for stock in prices:
        save_stock_price(stock)

    excluded_asset_types = ["Bond ETF"]

    alert_stocks = [
        stock for stock in prices
        if (
            stock["action"] is not None
            or stock["ma_alert"] is not None
        )
        and stock["asset_type"] not in excluded_asset_types
    ]

    send_stock_alert(
        alert_stocks=alert_stocks,
        market_name=market_name,
        total_count=len(watchlist),
        success_count=len(prices),
        failed_count=len(failed_stocks)
    )

    print(f"LINE stock summary sent: {len(alert_stocks)} alert stocks")

    write_github_summary(
        market_name=market_name,
        total_count=len(watchlist),
        success_count=len(prices),
        failed_count=len(failed_stocks),
        alert_count=len(alert_stocks),
        line_sent=True
    )

    print(f"Saved {len(prices)} stocks to DynamoDB")


def run_with_error_handling(target_market=None):
    try:
        run_workflow(target_market)
    except Exception:
        error_message = traceback.format_exc()
        send_workflow_failed_alert(error_message)
        raise