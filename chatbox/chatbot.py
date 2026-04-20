import json
import pickle
import random

from flask import Flask, request, jsonify, render_template_string

# ── Cargar modelo entrenado ────────────────────────────
MODELO_PATH = "modelo_chatbot.pkl"

try:
    with open(MODELO_PATH, "rb") as f:
        datos = pickle.load(f)
    pipeline   = datos["pipeline"]
    respuestas = datos["respuestas"]
    print("✔ Modelo cargado correctamente.")
except FileNotFoundError:
    raise RuntimeError("No se encontró el modelo. Ejecuta primero: python entrenar.py")

UMBRAL_CONFIANZA = 0.30   # si la probabilidad es menor, responde con "desconocido"

# ── Función principal de respuesta ────────────────────
def obtener_respuesta(mensaje: str) -> str:
    texto = mensaje.lower().strip()

    if not texto:
        return "Por favor escribe algo para poder ayudarte."

    # Predecir clase y probabilidad
    tag         = pipeline.predict([texto])[0]
    probabilidad = pipeline.predict_proba([texto]).max()

    if probabilidad < UMBRAL_CONFIANZA:
        tag = "desconocido"

    opciones = respuestas.get(tag, respuestas.get("desconocido", ["No entiendo lo que dices, escribe algo mas."]))
    return random.choice(opciones)

# ── Flask App ──────────────────────────────────────────
app = Flask(__name__)


@app.route("/chat", methods=["POST"])
def chat():
    """Endpoint principal del chatbot — recibe JSON y devuelve respuesta."""
    body    = request.get_json(force=True, silent=True) or {}
    mensaje = body.get("mensaje", "").strip()

    if not mensaje:
        return jsonify({"respuesta": "No recibí ningún mensaje. ¿Puedes escribir algo?"}), 400

    respuesta = obtener_respuesta(mensaje)
    return jsonify({"respuesta": respuesta})


@app.route("/webhook", methods=["POST"])
def webhook_twilio():
    from twilio.twiml.messaging_response import MessagingResponse
    mensaje_entrante = request.values.get("Body", "")
    respuesta_texto  = obtener_respuesta(mensaje_entrante)
    resp = MessagingResponse()
    resp.message(respuesta_texto)
    response = app.make_response(str(resp))
    response.headers["Content-Type"] = "application/xml"
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response


# ── Detectar webhook de ngrok ──────────────────────────
def obtener_url_ngrok():
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=3) as r:
            data = json.loads(r.read().decode())
            tunnels = data.get("tunnels", [])
            for t in tunnels:
                if t.get("proto") == "https":
                    return t["public_url"]
    except Exception:
        return None

# ── Ejecución ──────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Chatbot corriendo en http://localhost:5000")

    url_ngrok = obtener_url_ngrok()
    if url_ngrok:
        print(f"\n✅ Tu webhook para Twilio es:")
        print(f"   👉  {url_ngrok}/webhook\n")
    else:
        print("\n ngrok no detectado. Ejecuta ngrok en otra terminal:")
        print("      ngrok http 5000")
        print("   Luego reinicia este script para ver el webhook.\n")

    app.run(host="0.0.0.0", port=5000, debug=True)