from flask import Flask, request, jsonify, Response
import requests
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# Завдання 2: Простий GET-запит
@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World!"

# Завдання 3: GET-запит зі шляхом та параметрами (Кинути запит: .../currency?key=today)
@app.route("/currency", methods=["GET"])
def static_currency():
    param = request.args.get("key", "default")
    if param == "today":
        return "USD - 41.5"
    else:
        return f"Invalid parameter: {param}"

# Завдання 4: Обробка заголовків (Кинути запит: .../content?content_type=application/xml)
@app.route("/content", methods=["GET"])
def content_handler():
    # Перевірка заголовка Content-Type
    content_type = request.headers.get("Content-Type")
    
    # Альтернативна перевірка через параметр URL
    url_param_content_type = request.args.get("content_type")

    # Визначення типу на основі заголовка або параметра URL
    content_type = url_param_content_type if url_param_content_type else content_type

    if content_type == "application/json":
        return jsonify({"message": "This is JSON content"})
    elif content_type == "application/xml":
        xml_response = """<response><message>This is XML content</message></response>"""
        return Response(xml_response, mimetype="application/xml")
    else:
        return "This is plain text content"


# Завдання 5: Динамічний курс валют із НБУ (Кинути запит: .../currency_dynamic?param=today)
@app.route("/currency_dynamic", methods=["GET"])
def dynamic_currency():
    param = request.args.get("param")
    if param not in ["today", "yesterday"]:
        return "Invalid parameter. Use 'today' or 'yesterday'."

    date = datetime.now()
    if param == "yesterday":
        date -= timedelta(days=1)

    formatted_date = date.strftime("%Y%m%d")
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={formatted_date}&json"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return f"USD - {data[0]['rate']}"
        else:
            return "No data available."
    else:
        return f"Error fetching data: {response.status_code}"

if __name__ == "__main__":
    app.run(port=8000) # Завдання 1
