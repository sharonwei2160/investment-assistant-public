import requests

from config import LINE_CHANNEL_ACCESS_TOKEN


def send_message(message):
    url = "https://api.line.me/v2/bot/message/broadcast"

    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)

    print(response.status_code)
    print(response.text)

    if response.status_code >= 400:
        raise Exception(f"LINE message failed: {response.text}")


def send_stock_alert(
    alert_stocks,
    market_name,
    total_count=None,
    success_count=None,
    failed_count=None
):
    message = f"📉 股票監控提醒｜{market_name}\n\n"

    if total_count is not None:
        message += f"監控股票：{total_count}\n"

    if success_count is not None:
        message += f"成功抓取：{success_count}\n"

    if failed_count is not None:
        message += f"失敗檔數：{failed_count}\n"

    message += f"符合條件：{len(alert_stocks)}\n\n"

    if not alert_stocks:
        message += "✅ 今日沒有符合條件的股票。"
        send_message(message)
        return

    for stock in alert_stocks:
        message += (
            f'今天日期：{stock["date"]}\n'
            f'股票代碼：{stock["symbol"]}\n'
            f'股票名稱：{stock["name"]}\n'
            f'歷史最高價：{stock["historical_high"]}\n'
            f'歷史最高價日期：{stock["historical_high_date"]}\n'
            f'今天收盤價：{stock["close"]}\n'
            f'距離高點跌幅：{stock["drop_from_high_pct"]}%\n'
            f'跌幅行動：{stock["action"] or "無"}\n'
            f'月線 MA20：{stock["ma_month"]}\n'
            f'季線 MA60：{stock["ma_quarter"]}\n'
            f'年線 MA240：{stock["ma_year"]}\n'
            f'均線提醒：{stock["ma_alert"] or "無"}\n'
            f'--------------------\n'
        )

    send_message(message)


def send_fetch_failed_alert(failed_stocks, market_name):
    message = f"⚠️ 股票抓取失敗｜{market_name}\n\n"
    message += f"失敗檔數：{len(failed_stocks)}\n\n"

    for stock in failed_stocks:
        message += (
            f'股票代碼：{stock["symbol"]}\n'
            f'股票名稱：{stock.get("name")}\n'
            f'Yahoo 代碼：{stock["yahoo_symbol"]}\n'
            f'原因：{stock["reason"]}\n'
            f'--------------------\n'
        )

    send_message(message)


def send_workflow_failed_alert(error_message):
    message = (
        "🚨 Stock Workflow Failed\n\n"
        "錯誤內容：\n"
        f"{error_message[-1500:]}"
    )

    send_message(message)