from flask import Flask, request

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