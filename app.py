from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Diccionario para almacenar sesiones temporales por correo
temp_sessions = {}

@app.route('/')
def home():
    return "✅ API funcionando en Render"

# Endpoint para generar un correo temporal
@app.route('/mail', methods=['GET'])
def generar_mail():
    try:
        headers = {
            "Content-Type": "application/json"
        }

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
        }, headers=headers)

        data = resp.json()

        if "errors" in data:
            return {"error": "❌ Error en la API de Dropmail"}, 500

        session_id = data["data"]["introduceSession"]["id"]
        address = data["data"]["introduceSession"]["addresses"][0]["address"]

        # Guardamos en memoria
        temp_sessions[address] = session_id

        return {"email": address}
    
    except Exception as e:
        return {"error": f"❌ Fallo al generar correo: {str(e)}"}, 500

# Endpoint para revisar correos (a completar)
@app.route('/msj', methods=['GET'])
def revisar_mensajes():
    return {"mensaje": "🔍 Aún no implementado"}
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
