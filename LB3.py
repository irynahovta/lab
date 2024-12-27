from flask import Flask, request, jsonify, Response, abort
from flask_httpauth import HTTPBasicAuth
import sqlite3

app = Flask(__name__)
auth = HTTPBasicAuth()

# Імітація бази користувачів
users = {
    "admin": "password",
    "user": "1234"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# Збереження товарів у базі даних SQLite
DATABASE = "catalog.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Кореневий маршрут
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Items API. Use /items to interact with the catalog."})

# Ендпоінт для роботи з усіма товарами
@app.route("/items", methods=["GET", "POST"])
@auth.login_required
def items():
    if request.method == "GET":
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        conn.close()
        return jsonify([{"id": item[0], "name": item[1], "price": item[2], "description": item[3]} for item in items])

    if request.method == "POST":
        data = request.get_json()
        if not data or "name" not in data or "price" not in data:
            abort(400, "Invalid data")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, price, description) VALUES (?, ?, ?)", (data["name"], data["price"], data.get("description", "")))
        conn.commit()
        conn.close()
        return jsonify({"message": "Item created successfully"}), 201

# Ендпоінт для роботи з конкретним товаром за ID
@app.route("/items/<int:item_id>", methods=["GET", "PUT", "DELETE"])
@auth.login_required
def item_by_id(item_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()
        if not item:
            abort(404, "Item not found")
        return jsonify({"id": item[0], "name": item[1], "price": item[2], "description": item[3]})

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            abort(400, "Invalid data")

        cursor.execute(
            "UPDATE items SET name = ?, price = ?, description = ? WHERE id = ?",
            (data.get("name"), data.get("price"), data.get("description"), item_id)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Item updated successfully"})

    if request.method == "DELETE":
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Item deleted successfully"})

if __name__ == "__main__":
    app.run(port=8000)
