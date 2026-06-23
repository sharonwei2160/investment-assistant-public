# 📈 Stock Alert System

![Workflow](https://github.com/<USERNAME>/stock-alert-system/actions/workflows/stock-alert.yml/badge.svg)
An automated stock monitoring system that tracks Taiwan and US stocks, stores historical prices in DynamoDB, and sends LINE notifications when predefined investment conditions are met.

---

## 🚀 Features

- 📊 Retrieve daily stock prices from Yahoo Finance
- 🇹🇼 Monitor Taiwan market after close (14:00 Taiwan Time)
- 🇺🇸 Monitor US market after close (07:00 Taiwan Time)
- 💾 Store historical prices in Amazon DynamoDB
- 📱 Send LINE notifications when price drops from historical high
- ⚠️ Notify when stock data retrieval fails
- 🚨 Notify when workflow execution fails
- 🤖 Automated daily execution using GitHub Actions

---

## 🏗 Architecture

```text
                GitHub Actions
              (07:00 / 14:00)

                     │
                     ▼

              Python Application

        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼

 Yahoo Finance   DynamoDB      LINE Bot
  (Market Data)  (History)   (Notification)
```

---

## 📂 Project Structure

```text
stock-alert-system
│
├── .github
│   └── workflows
│       └── stock-alert.yml      # GitHub Actions workflow
│
├── app
│   ├── main.py                  # Application entry point
│   ├── config.py                # Configuration
│   ├── stock_service.py         # Yahoo Finance integration
│   ├── aws_service.py           # DynamoDB operations
│   ├── line_service.py          # LINE Messaging API
│   ├── get_line_user_id.py      # LINE utility
│   └── watchlist.json           # Portfolio watchlist
│
├── data                         # Local cache (optional)
├── docs                         # Documentation
├── logs                         # Log files
├── tableau                      # Tableau dashboards
├── tests                        # Unit tests
│
├── .env.example                 # Environment variable template
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙ Tech Stack

- Python 3.13
- GitHub Actions
- Amazon DynamoDB
- Yahoo Finance (yfinance)
- LINE Messaging API
- boto3

---

## 🔔 Notification Rules

Notifications are sent only when:

| Drop from Historical High | Action |
|--------------------------:|--------|
| ≥ 2% | Test notification |
| ≥ 5% | Drop 5% |
| ≥ 10% | Drop 10% - Consider buying |
| ≥ 20% | Drop 20% - Strong Buy |
| ≥ 30% | Drop 30% - Buy Aggressively |

Bond ETFs are excluded from notifications.

---

## 📱 LINE Notification Example

```text
📈 Stock Alert

📅 Date: 2026-06-21

Ticker: 2330
Name: TSMC

Historical High:
1160
2024-07-11

Today's Close:
1023

Drop from ATH:
11.81%

Action:
🟠 Drop 10% - Consider buying
```

---

## 🔄 Workflow

```text
GitHub Actions

        │

        ▼

Download Stock Prices

        │

        ▼

Calculate Historical High

        │

        ▼

Save to DynamoDB

        │

        ▼

Check Alert Rules

        │

        ▼

LINE Notification
```

---

## 📅 Automation Schedule

| Market | Taiwan Time | GitHub Actions |
|---------|-------------|----------------|
| Taiwan | 14:00 | Weekdays |
| US | 07:00 | Weekdays |

---

## 📌 Future Roadmap

- [ ] Dividend Yield
- [ ] PE Ratio
- [ ] RSI
- [ ] Moving Average (MA20 / MA60)
- [ ] Fear & Greed Index
- [ ] AI Buy Recommendation
- [ ] Portfolio Dashboard
- [ ] Performance Analytics

---

## 👤 Author

Sharon Wei

Senior Business Analyst

Built with Python, GitHub Actions, DynamoDB and LINE Messaging API.
