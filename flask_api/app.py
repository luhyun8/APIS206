from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

API = "http://127.0.0.1:5000/v1/Usuarios"
DELETE_AUTH = ("Guadalupe", "BTS")

# Página principal
@app.route("/")
def index():
    usuarios = []
    try:
        response = requests.get(API, timeout=10)
        response.raise_for_status()
        data = response.json()
        usuarios = data.get("data", [])
    except requests.RequestException:
        # Si el backend no responde, se muestra la tabla vacia en lugar de romper la vista.
        usuarios = []
    return render_template("index.html", usuarios=usuarios)

# Crear usuario
@app.route("/crear", methods=["POST"])
def crear_usuario():
    nuevo_usuario = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }

    requests.post(API, json=nuevo_usuario, timeout=10)
    return redirect("/")

# Eliminar usuario
@app.route("/eliminar/<int:id>")
def eliminar_usuario(id):
    requests.delete(f"{API}/{id}", auth=DELETE_AUTH, timeout=10)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5010)