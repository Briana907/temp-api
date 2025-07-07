from flask import Flask, request
import requests
import os

app = Flask(__name__)

temp_sessions = {}  # Sesiones por IP o algún identificador si deseas

@app.route('/')
def home():
    return "✅ API funcionando en Render"

@app.route('/mail', methods=['GET'])
def generar_mail():
    resp = requests.post("https://dropmail.me/api/graphql", json={
        "query": "mutation { introduceSession { id, addresses { address } } }"
    })

    data = resp.json()
    session_id = data["data"]["introduceSession"]["id"]
    address = data["data"]["introduceSession"]["addresses"][0]["address"]

    # Guardamos sesión en memoria
    temp_sessions[address] = session_id

    return {"email": address}

@app.route('/msj', methods=['GET'])
def revisar_msj():
    email = request.args.get("email")  # ejemplo: /msj?email=xxx@yyy.com
    session_id = temp_sessions.get(email)

    if not session_id:
        return {"mensaje": "Correo no válido o no registrado"}

    resp = requests.post("https://dropmail.me/api/graphql", json={
        "query": f'query {{ session(id: "{session_id}") {{ mails {{ fromAddr, subject, text }} }} }}'
    })

    mails = resp.json().get("data", {}).get("session", {}).get("mails", [])

    if not mails:
        return {"mensaje": "Sin nuevos correos"}

    # Solo muestra el primero (puedes mostrar todos si quieres)
    mail = mails[0]
    return {
        "de": mail.get("fromAddr", "Desconocido"),
        "asunto": mail.get("subject", "Sin asunto"),
        "mensaje": mail.get("text", "")[:1000]
    }

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
