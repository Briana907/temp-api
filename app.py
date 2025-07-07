from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Diccionario para guardar sesiones temporales por dirección de correo
temp_sessions = {}

@app.route('/')
def home():
    return "✅ API funcionando en Render"

# Endpoint para generar correo temporal
@app.route('/mail', methods=['GET'])
def generar_mail():
    try:
        resp = requests.post("https://dropmail.me/api/graphql", json={
            "query": """
                mutation {
                    introduceSession {
                        id
                        addresses {
                            address
                        }
                    }
                }
            """
        })

        data = resp.json()

        if "errors" in data:
            return {"error": "❌ Error en la API de Dropmail"}, 500

        session_id = data["data"]["introduceSession"]["id"]
        address = data["data"]["introduceSession"]["addresses"][0]["address"]

        # Guardamos la sesión usando el correo como clave
        temp_sessions[address] = session_id

        return {"email": address}
    
    except Exception as e:
        return {"error": f"❌ Fallo al generar correo: {str(e)}"}, 500

# Endpoint para revisar mensajes del correo generado
@app.route('/msj', methods=['GET'])
def revisar_mensajes():
    email = request.args.get("email")

    if not email or email not in temp_sessions:
        return {"mensaje": "❌ Correo no válido o no encontrado"}, 400

    session_id = temp_sessions[email]

    try:
        resp = requests.post("https://dropmail.me/api/graphql", json={
            "query": f"""
                query {{
                    session(id: "{session_id}") {{
                        mails {{
                            id
                            fromAddr
                            subject
                            text
                        }}
                    }}
                }}
            """
        })

        data = resp.json()

        mails = data.get("data", {}).get("session", {}).get("mails", [])

        if not mails:
            return {"mensaje": "📭 Sin nuevos correos"}

        # Solo mostramos el último correo por simplicidad
        ultimo = mails[-1]
        resumen = {
            "de": ultimo["fromAddr"],
            "asunto": ultimo["subject"],
            "contenido": ultimo["text"][:300]  # Cortamos por si es muy largo
        }

        return resumen

    except Exception as e:
        return {"error": f"❌ Fallo al revisar mensajes: {str(e)}"}, 500

# Para asegurar que funcione en Render (puerto dinámico)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
