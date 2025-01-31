# Backend Documentation

## **1. Tech Stack**

| Category                    | Choice                | Reasoning                                                                                       |
| --------------------------- | --------------------- | ----------------------------------------------------------------------------------------------- |
| **Backend Framework** | Python + FastAPI      | Async-ready, lightweight, and aligns with[Alpaca.py/LangChain](http://alpaca.py/LangChain)tooling. |
| **Database**          | PostgreSQL (Supabase) | Relational structure for trades/user data; integrates with Clerk auth.                          |
| **Authentication**    | Clerk (JWT tokens)    | Session management handled by Clerk; backend validates tokens.                                  |
| **API Design**        | RESTful               | Simpler to implement for MVP vs. GraphQL; aligns with Alpaca’s APIs.                           |

---

## **2. Third-Party Integrations**

1. **Alpaca API** :

* Paper trading endpoints for MVP.

1. **Groq** :

* LLM processes natural language into structured trade commands.

1. **Clerk** :

* Validate JWT tokens on every API request.

1. **Paddle** :

* Handle donation payments via webhooks

---

# 3. **Critical Flows**

### **Trade Execution**

1. User sends command (e.g., “Buy $100 BTC”) via frontend.
2. Backend sends command to Groq for parsing.
3. LangChain validates command structure (symbol, action, amount).
4. Validated command → Alpaca API execution.

### **Authentication**

1. Frontend sends Clerk session token in `Authorization` header.
2. Backend verifies token via Clerk’s public API.
3. User ID mapped to Alpaca account for trading.

## **4. Deployment**

* **Hosting (both front and backend)** : Render
