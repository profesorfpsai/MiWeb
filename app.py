from flask import Flask, render_template, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

# Página principal (HTML dinámico)
@app.route("/")
def home():
    return render_template("index.html")

# API para clientes
@app.route("/clientes")
def clientes():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM clientes")
    rows = cur.fetchall()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "nombre": r[1],
            "email": r[2],
            "telefono": r[3]
        })

    cur.close()
    conn.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run()