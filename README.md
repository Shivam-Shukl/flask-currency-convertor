# 💱 Telegram Currency Converter Bot – `ramukakabot`

This is a simple yet powerful Telegram bot that converts currencies using real-time exchange rates via the [ExchangeRate API](https://www.exchangerate-api.com/). It uses:

- 🧠 **Dialogflow** for intent understanding
- 🌐 **Flask** backend deployed on **Render**
- 🤖 Telegram bot interface
- 📊 Real-time currency conversion

---

## ✅ Features

- Convert between major currencies (e.g. USD to INR, INR to PKR, etc.)
- Friendly conversational replies via Dialogflow
- Lightweight Flask server with webhook integration
- Deployed seamlessly on Render.com

---

## 🚀 How it works

1. User sends message to Telegram bot (e.g., "200 USD to INR")
2. Dialogflow parses the intent and extracts parameters
3. Flask backend receives the request via webhook
4. Backend fetches live exchange rates from [open.er-api.com](https://open.er-api.com/)
5. Returns the converted currency value to Telegram via Dialogflow

---

## 🛠 Setup Guide

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/telegram-currency-bot.git
cd telegram-currency-bot
```

### 2. Install dependencies

```bash
pip install flask requests
```

### 3. Create `main.py` with this code

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    try:
        unit_currency = data['queryResult']['parameters']['unit-currency'][0]
        source_currency = unit_currency['currency'].upper()
        amount = float(unit_currency['amount'])
        target_currency = data['queryResult']['parameters']['currency-name'].upper()

        url = f"https://open.er-api.com/v6/latest/{source_currency}"
        response = requests.get(url)
        exchange_data = response.json()

        if exchange_data.get("result") != "success":
            raise Exception("Failed to fetch exchange rate")

        rate = exchange_data['rates'].get(target_currency)

        if not rate:
            raise Exception(f"Currency '{target_currency}' not supported.")

        converted_amount = round(amount * rate, 2)
        message = f"{amount} {source_currency} = {converted_amount} {target_currency}"

        return jsonify({"fulfillmentText": message})

    except Exception as e:
        return jsonify({"fulfillmentText": "Something went wrong. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
```

---

### 4. Deploy on Render

- Push the code to GitHub
- Go to [Render.com](https://render.com/)
- Select **Web Service** > Connect your repo
- Use:
  - Runtime: Python
  - Start command: `gunicorn main:app`

---

### 5. Setup Dialogflow Webhook

- Go to Dialogflow → Fulfillment
- Enable webhook and paste your Render deployment URL (e.g. `https://your-bot.onrender.com`)
- Go to Intents > Currency Converter
  - Use parameters: `unit-currency`, `currency-name`
- Enable webhook call for this intent

---

### 6. Connect with Telegram

- Create a bot via [BotFather](https://t.me/BotFather)
- Name: `ramukakabot`
- Username: `@RAmmmu_kaka_bot`
- Connect to Dialogflow via **Integrations → Telegram**

---

## 📸 Screenshots

### Telegram Bot in Action


```
<img src="https://github.com/user-attachments/assets/5b2b7b5d-b554-44a5-abe9-b5a95db0b6ae" width="600"/>
<img src="https://github.com/user-attachments/assets/e692603f-977f-4ac4-8ecc-8c8f62b13600" width="600"/>


```

---

## 📎 To-Do

- Add support for multiple languages
- Improve error messages
- Add logs and analytics dashboard

---

## 👨‍💻 Author

Created with ❤️ by Shivam 
