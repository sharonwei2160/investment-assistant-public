import traceback

import yfinance as yf


def get_action(drop_pct):
    if drop_pct >= 30:
        return "跌30%，買啊買啊"
    elif drop_pct >= 20:
        return "跌20%，進場囉!"
    elif drop_pct >= 10:
        return "跌10%，留意了"
    else:
        return None


def get_ma_alerts(close_price, ma_month, ma_quarter, ma_year):
    alerts = []

    below_ma_month = close_price < ma_month
    below_ma_quarter = close_price < ma_quarter
    below_ma_year = close_price < ma_year

    if below_ma_month:
        alerts.append("跌破月線")

    if below_ma_quarter:
        alerts.append("跌破季線")

    if below_ma_year:
        alerts.append("跌破年線")

    return {
        "below_ma_month": below_ma_month,
        "below_ma_quarter": below_ma_quarter,
        "below_ma_year": below_ma_year,
        "ma_alert": "、".join(alerts) if alerts else None
    }


def get_stock_prices(watchlist):
    results = []
    failed_stocks = []

    for stock in watchlist:
        symbol = stock["symbol"]
        yahoo_symbol = stock.get("yahoo_symbol", symbol)

        try:
            print(f"Fetching {symbol} using {yahoo_symbol}")

            ticker = yf.Ticker(yahoo_symbol)
            history = ticker.history(period="max")

            if history.empty:
                failed_stocks.append({
                    "symbol": symbol,
                    "yahoo_symbol": yahoo_symbol,
                    "name": stock.get("name"),
                    "reason": "No price data found"
                })
                print(f"❌ No data found: {symbol} ({yahoo_symbol})")
                continue

            latest = history.iloc[-1]
            today_date = history.index[-1].strftime("%Y-%m-%d")

            close_price = float(latest["Close"])

            historical_high = float(history["High"].max())
            historical_high_date = history["High"].idxmax().strftime("%Y-%m-%d")

            drop_from_high_pct = round(
                (historical_high - close_price) / historical_high * 100,
                2
            )

            ma_month = float(history["Close"].tail(20).mean())
            ma_quarter = float(history["Close"].tail(60).mean())
            ma_year = float(history["Close"].tail(240).mean())

            ma_info = get_ma_alerts(
                close_price=close_price,
                ma_month=ma_month,
                ma_quarter=ma_quarter,
                ma_year=ma_year
            )

            action = get_action(drop_from_high_pct)

            results.append({
                "date": today_date,
                "symbol": symbol,
                "yahoo_symbol": yahoo_symbol,
                "name": stock.get("name"),
                "market": stock.get("market"),
                "asset_type": stock.get("asset_type"),
                "currency": stock.get("currency"),
                "historical_high": round(historical_high, 2),
                "historical_high_date": historical_high_date,
                "close": round(close_price, 2),
                "drop_from_high_pct": drop_from_high_pct,
                "action": action,
                "ma_month": round(ma_month, 2),
                "ma_quarter": round(ma_quarter, 2),
                "ma_year": round(ma_year, 2),
                "below_ma_month": ma_info["below_ma_month"],
                "below_ma_quarter": ma_info["below_ma_quarter"],
                "below_ma_year": ma_info["below_ma_year"],
                "ma_alert": ma_info["ma_alert"]
            })

            print(
                f"✅ Success: {symbol}, "
                f"close: {round(close_price, 2)}, "
                f"drop: {drop_from_high_pct}%, "
                f"action: {action}, "
                f"ma_alert: {ma_info['ma_alert']}"
            )

        except Exception as error:
            failed_stocks.append({
                "symbol": symbol,
                "yahoo_symbol": yahoo_symbol,
                "name": stock.get("name"),
                "reason": str(error),
                "traceback": traceback.format_exc()
            })
            print(f"❌ Failed: {symbol} ({yahoo_symbol}) - {error}")

    print(f"Total success: {len(results)} / {len(watchlist)}")
    print(f"Total failed: {len(failed_stocks)} / {len(watchlist)}")

    return results, failed_stocks