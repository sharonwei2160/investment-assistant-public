# 📈 Stock Decision System

An automated investment monitoring system that tracks Taiwan and US stocks, manages portfolio allocation and capital pools, generates daily investment recommendations, and delivers investment reports through Email and LINE.

The project started as a simple stock alert system and is gradually evolving into a modular investment decision engine.

---

# 🚀 Current Features

### 📊 Market Monitoring

* Retrieve daily Taiwan and US stock prices from Yahoo Finance
* Monitor Taiwan market after close (14:00 Taiwan Time)
* Monitor US market after close (07:00 Taiwan Time)
* Store historical prices in Amazon DynamoDB
* Calculate drawdown from historical highs
* Detect moving average signals
* Separate stock and bond ETF monitoring

### 💼 Portfolio Management

* Track portfolio holdings
* Calculate current portfolio allocation
* Compare current allocation with target allocation
* Track multiple investment capital pools
* Calculate deposited, invested and remaining capital

### 💡 Investment Recommendation

* Generate stock-level investment recommendations
* Generate Daily Investment Brief
* Build plain-text investment emails
* Send investment reports by Email
* Send stock alerts through LINE
* Automated daily execution using GitHub Actions

---

# 🏗 Current Architecture

```text
                    GitHub Actions
                 (Daily Scheduled Run)

                         │
                         ▼

                  Python Application

        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼

 Yahoo Finance     Portfolio      Capital Manager
  Market Data         Data          (Fund Balance)

        │              │              │
        └──────────────┼──────────────┘
                       ▼

              Recommendation Service

                       │
                       ▼

               Daily Report Builder

                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼

     Email Builder               LINE Alert
```

---

# 📂 Project Structure

```text
stock-alert-system
│
├── .github
│   └── workflows
│       └── stock-alert.yml
│
├── app
│   ├── main.py
│   ├── config.py
│   │
│   ├── stock_service.py
│   ├── drawdown_service.py
│   ├── aws_service.py
│   │
│   ├── portfolio_engine.py
│   ├── capital_manager.py
│   ├── recommendation_service.py
│   │
│   ├── report_builder.py
│   ├── email_builder.py
│   ├── email_sender.py
│   │
│   ├── line_service.py
│   ├── watchlist.json
│   └── portfolio.json
│
├── data
├── docs
├── logs
├── tableau
├── tests
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

# ⚙ Tech Stack

* Python 3.13
* GitHub Actions
* Amazon DynamoDB
* Yahoo Finance (`yfinance`)
* Amazon SES / SMTP
* LINE Messaging API
* boto3
* pandas
* openpyxl

---

# 🔔 Alert Rules

Notifications are sent when the stock price reaches predefined drawdown levels.

| Drawdown from Historical High | Action            |
| ----------------------------: | ----------------- |
|                          ≥ 2% | Test Notification |
|                          ≥ 5% | Monitor           |
|                         ≥ 10% | Consider Buying   |
|                         ≥ 20% | Strong Buy        |
|                         ≥ 30% | Buy Aggressively  |

Bond ETFs are excluded from drawdown notifications.

---

# 📧 Daily Investment Brief

The system automatically generates a daily investment report including:

* Portfolio summary
* Capital pool balances
* Available investment capital
* Stock recommendations
* Moving average alerts
* Market statistics

---

# 🔄 Current Workflow

```text
GitHub Actions

        │

        ▼

Download Market Data

        │

        ▼

Update Historical Prices

        │

        ▼

Update Portfolio Status

        │

        ▼

Update Capital Status

        │

        ▼

Generate Recommendations

        │

        ▼

Build Daily Report

        │

        ▼

Email Report

        │

        ▼

LINE Alert
```

---

# 📅 Automation Schedule

| Market | Taiwan Time | Schedule |
| ------ | ----------- | -------- |
| Taiwan | 14:00       | Weekdays |
| US     | 07:00       | Weekdays |

---

# 🚧 Project Status

**Current Version:** V1

Current capabilities:

* ✅ Daily stock monitoring
* ✅ Portfolio tracking
* ✅ Capital management
* ✅ Investment recommendations
* ✅ Daily email reports
* ✅ LINE notifications
* ✅ GitHub Actions automation

---

# 🛣 Roadmap

The next milestone is to evolve this project from a monitoring system into a modular investment decision engine.

## Phase 1 — Decision Engine

* [ ] Need Score
* [ ] Opportunity Score
* [ ] Decision Engine
* [ ] Allocation Engine

## Phase 2 — Market Strategy

* [ ] Market State
* [ ] Dynamic deployment rules
* [ ] Portfolio health analysis
* [ ] Risk management

## Phase 3 — Presentation

* [ ] Improved email layout
* [ ] HTML email template
* [ ] Rich LINE messages

## Phase 4 — Productization

* [ ] Deployment simulation
* [ ] Dashboard
* [ ] Backtesting
* [ ] AI-assisted investment insights

---

# 👤 Author

**Sharon Wei**

Senior Business Analyst

Built with Python, GitHub Actions, Amazon DynamoDB, Yahoo Finance and LINE Messaging API.
