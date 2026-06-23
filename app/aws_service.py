import boto3
from decimal import Decimal

from config import AWS_REGION, DYNAMODB_TABLE_NAME

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def save_stock_price(stock):
    item = {
        "symbol": stock["symbol"],
        "price_date": stock["date"],
        "yahoo_symbol": stock["yahoo_symbol"],
        "name": stock["name"],
        "market": stock["market"],
        "asset_type": stock["asset_type"],
        "currency": stock["currency"],
        "historical_high": Decimal(str(stock["historical_high"])),
        "historical_high_date": stock["historical_high_date"],
        "close": Decimal(str(stock["close"])),
        "drop_from_high_pct": Decimal(str(stock["drop_from_high_pct"])),
        "action": stock["action"] or "",
        "ma_month": Decimal(str(stock["ma_month"])),
        "ma_quarter": Decimal(str(stock["ma_quarter"])),
        "ma_year": Decimal(str(stock["ma_year"])),
        "below_ma_month": stock["below_ma_month"],
        "below_ma_quarter": stock["below_ma_quarter"],
        "below_ma_year": stock["below_ma_year"],
        "ma_alert": stock["ma_alert"] or ""
    }

    table.put_item(Item=item)