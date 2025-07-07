from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
temp_sessions = {}  # Sesiones temporales por IP o dirección

@app.route('/')
def home():
    return "✅ API funcionando en Render"

@app.route('/mail', methods=['GET'])
def generar_mail():
    try:
        resp = requests.post(
            "https://dropmail.me/api/graphql",
            headers={"Content-Type": "application/json"},
            json={
                "query": "mutation { introduceSession { id, addresses { address } } }"
            }
        )

        data = resp.json()
        session_id = data["data"]["introduceSession"]["id"]
        address = data["data"]["introduceSession"]["addresses"][0]["address"]

        # Guardar en memoria por ahora
        temp_sessions[address] = session_id

        return jsonify({"email": address})

    except Exception as e:
        return jsonify({"error": f"❌ Fallo al generar correo: {str(e)}"}), 500

@app.route('/msj', methods=['GET'])
def revisar_msj():
    try:
        # Obtener correo desde el parámetro ?email=
        email = request.args.get("email")
        if not email:
            return jsonify({"error": "❌ No se especificó el correo."}), 400

        session_id = temp_sessions.get(email)
        if not session_id:
            return jsonify({"mensaje": "⚠️ No se encontró sesión activa para ese correo."})

        # Consultamos mensajes con la sesión
        resp = requests.post(
            "https://dropmail.me/api/graphql",
            headers={"Content-Type": "application/json"},
            json={
                "query": f"query {{ session(id: \"{session_id}\") {{ mails {{ rawText }} }} }}"
            }
        )

        data = resp.json()
        mails = data["data"]["session"]["mails"]

        if not mails:
            return jsonify({"mensaje": "📭 Sin nuevos correos"})

        mensajes = "\n\n".join(m["rawText"] for m in mails)
        return jsonify({"mensaje": mensajes})

    except Exception as e:
        return jsonify({"error": f"❌ Error al revisar mensajes: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
