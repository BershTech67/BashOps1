# Ironsail Prescription Intelligence API

A robust, asynchronous 20% prototype demonstrating AI-powered prescription verification, drug interaction checking, and pharmacy infrastructure. Built for Ironsail.

## 🚀 Features
- **FastAPI Backend:** Fully asynchronous endpoints relying on `asyncpg` and SQLAlchemy 2.0.
- **AI Interaction Checking:** Utilizes the Groq API (Llama 3) to analyze complex drug contraindications and return structured JSON clinical warnings.
- **Inventory Mocks:** Simulates pharmacy stock checks and alternative generic routing.

## 🛠 Tech Stack
- Python 3.10+
- FastAPI & Uvicorn
- PostgreSQL (Async)
- Groq AI API

## ⚙️ Quick Start

1. **Clone & Install**
```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
