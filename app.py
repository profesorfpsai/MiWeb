import os
from flask import Flask, jsonify, request, render_template
import psycopg2

app = Flask(__name__)

# 🔗 Conexión a PostgreSQL (Render usa DATABASE_URL)
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


# 🏠 Ruta principal
@app.route("/")
def home():
    return render_template("index.html")


# 📋 Obtener todos los clientes
@app.route("/clientes", methods=["GET"])
def get_clientes():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, nombre, email FROM clientes;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    clientes = [
        {"id": r[0], "nombre": r[1], "email": r[2]}
        for r in rows
    ]

    return jsonify(clientes)


# ➕ Crear cliente
@app.route("/clientes", methods=["POST"])
def create_cliente():
    data = request.get_json()
    nombre = data["nombre"]
    email = data["email"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO clientes (nombre, email) VALUES (%s, %s) RETURNING id;",
        (nombre, email)
    )

    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"id": new_id, "nombre": nombre, "email": email})


# 🚀 IMPORTANTE PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)