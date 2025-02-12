# Kryptt 🌍💸

_Democratizing global trading for Jamaican investors through AI-powered automation_

## Problem Statement 💡

Jamaican residents face:

- 🚫 Limited access to intuitive global trading platforms
- 📉 Overwhelming manual interfaces for casual investors
- 🇯🇲 Lack of local banking integration for international markets

## Key Features 🚀

- **Alpaca Integration** 🔌: SEC-licensed trading with Jamaican KYC compliance
- **Natural Language Trading** 🤖: "Buy $50 AAPL" commands via Groq's ultra-fast LLM
- **Clerk Authentication** 🔒: Secure user management with JWT sessions
- **Donation System** ❤️: Paddle integration for platform support

# Quick Start 🛠️

## Install dependencies

```powershell
pip install -r requirements.txt
```

## Configure trading environment

```powershell
cp .env.example .env
```

## Starting the backend server

```python-repl
uvicorn app.main:app --reload --port 8000
```

## Starting the frontend

```typescript
npm install
npm run dev
```

## Core Tech Stack ⚙️

`Alpaca API` · `Supabase` · `Groq` · `LangGraph` · `FastAPI`

## Roadmap 🗺️

- [X] JMD-denominated portfolio view
- [ ] Recurring orders ("Buy every Monday")
- [ ] WhatsApp trading integration
- [ ] Trading based on monetary events (e.g. "Buy $50 ETHUSD when it hits $150")
- [ ] Trading based on social media (e.g. "Buy $50 DOGEUSD when ELON tweets")
- [ ] Trading based on technical analysis (e.g. "Buy $50 $BTCUSD if the RSI is below 30")

_Licensed under [GPLv3](LICENSE)_ • [Report Issue](https://github.com/jondoescoding/crypt/issues)
