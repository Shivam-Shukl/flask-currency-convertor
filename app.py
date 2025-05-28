from flask import Flask, request, jsonify
import requests
import pprint
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    pprint.pprint(data)  # Debug the full payload

    try:
        # Extract data safely
        unit_currency = data['queryResult']['parameters']['unit-currency'][0]
        source_currency = unit_currency['currency'].upper()
        amount = float(unit_currency['amount'])
        target_currency = data['queryResult']['parameters']['currency-name'].upper()

        print("Source Currency:", source_currency)
        print("Amount:", amount)
        print("Target Currency:", target_currency)

        # Call ExchangeRate API
        url = f"https://open.er-api.com/v6/latest/{source_currency}"
        response = requests.get(url)
        exchange_data = response.json()

        # Check success
        if exchange_data.get("result") != "success":
            raise Exception("Failed to fetch exchange rate")

        rate = exchange_data['rates'].get(target_currency)

        if not rate:
            raise Exception(f"Currency '{target_currency}' not supported.")

        converted_amount = amount * rate
        converted_amount = round(converted_amount, 2)

        message = f"{amount} {source_currency} = {converted_amount} {target_currency}"
        print(message)

        return jsonify({"fulfillmentText": message})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"fulfillmentText": "Something went wrong. Please check your currencies or try again later."})


if __name__ == "__main__":
    # 🟡 Use the PORT provided by Render, or default to 10000 locally
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
