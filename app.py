from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor en línea"

@app.route('/mail', methods=['GET'])
def generar_mail():
    # lógica para generar correo temporal
    return {"email": "usuario@temporal.com"}

@app.route('/msj', methods=['GET'])
def revisar_msj():
    # lógica para revisar correos
    return {"mensaje": "Sin nuevos correos"}

# ⚠️ ESTA PARTE ES LA QUE DEBES AGREGAR
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
