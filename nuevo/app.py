# =========================================
# CHATBOT DEL FORO ESTUDIANTIL
# =========================================
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

# =========================================
# DATOS DEL CHATBOT
# =========================================
NOMBRE_BOT    = "Asistente del Foro Estudiantil"
NOMBRE_EQUIPO = "Julián Aguilar y Emir Sarabia"

MENU = (
    f"Hola, soy {NOMBRE_BOT} 🤖\n\n"
    "Escribe una opción o palabra clave:\n"
    "1) ¿Qué es el foro?\n"
    "2) Categorías\n"
    "3) Cómo publicar\n"
    "4) Cómo responder\n"
    "5) Registro\n"
    "6) Reglas\n"
    "7) Ayuda\n"
    "8) Salir"
)

# =========================================
# FUNCIÓN PRINCIPAL DE RESPUESTA
# =========================================
def responder_mensaje(mensaje: str) -> str:
    texto = mensaje.lower().strip()

    if not texto:
        return "Por favor escribe algo para poder ayudarte."

    if texto in ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "hey", "holi"]:
        return (
            f"Hola, soy {NOMBRE_BOT} de {NOMBRE_EQUIPO}.\n\n"
            "Estoy para ayudarte con el Foro Estudiantil.\n\n"
            f"{MENU}"
        )

    elif texto in ["menu", "menú", "ayuda", "opciones", "7"]:
        return MENU

    elif texto in ["1", "foro", "que es el foro", "info"]:
        return (
            "Este es un foro estudiantil donde puedes conversar sobre temas\n"
            "escolares, hacer preguntas, responder a compañeros y compartir\n"
            "conocimiento por categorías."
        )

    elif texto in ["2", "categorias", "categorías", "secciones"]:
        return (
            "El foro tiene estas categorías:\n"
            "📚 General\n"
            "💻 Académico\n"
            "📖 Grupo de Estudio\n"
            "🌐 Carrera y Empleo\n"
            "💡 Proyectos\n"
            "🎉 Off-topic\n\n"
            "¡Explora cada una!"
        )

    elif texto in ["3", "publicar", "como publico", "nuevo tema", "postear"]:
        return (
            "Para publicar:\n"
            "1) Inicia sesión.\n"
            "2) Elige una categoría.\n"
            "3) Haz clic en 'Nuevo tema'.\n"
            "4) Escribe tu título y mensaje.\n"
            "5) ¡Publica!\n\n"
            "Así de fácil 😊"
        )

    elif texto in ["4", "responder", "comentar", "como respondo"]:
        return (
            "Para responder:\n"
            "Abre el tema que te interesa y al final encontrarás\n"
            "el campo para escribir tu respuesta.\n\n"
            "¡Comparte tu conocimiento!"
        )

    elif texto in ["5", "registro", "registrarse", "crear cuenta", "sign up"]:
        return (
            "Para registrarte:\n"
            "Haz clic en 'Registrarse' en la esquina superior derecha,\n"
            "llena el formulario con tu nombre, carrera, correo y\n"
            "contraseña. Recibirás un correo de confirmación.\n\n"
            "¡Listo!"
        )

    elif texto in ["6", "reglas", "normas", "politicas"]:
        return (
            "Desde la página principal puedes acceder a la pestaña\n"
            "de reglas del foro.\n\n"
            "Normas básicas:\n"
            "✔ Respeto entre usuarios\n"
            "✔ No spam\n"
            "✔ Lenguaje apropiado\n"
            "✔ Publicar en la categoría correcta"
        )

    elif texto in ["8", "salir", "adios", "adiós", "bye", "hasta luego"]:
        return "¡Hasta luego! Sigue participando en el foro 👋"

    elif "gracias" in texto:
        return "¡De nada! Para eso estoy 😊 ¿Hay algo más en que pueda ayudarte?"

    elif "reporte" in texto or "reportar" in texto or "inapropiado" in texto:
        return (
            "Puedes reportar contenido inapropiado usando el botón\n"
            "'Reportar' en cada publicación. Los moderadores lo revisarán."
        )

    elif "buscar" in texto or "buscador" in texto or "encontrar" in texto:
        return (
            "Usa la barra de búsqueda en la parte superior del foro\n"
            "para encontrar temas por palabras clave. 🔍"
        )

    elif "contraseña" in texto or "login" in texto or "iniciar sesion" in texto:
        return (
            "Para iniciar sesión usa tu correo y contraseña en el botón\n"
            "'Entrar'. Si olvidaste tu contraseña, usa la opción\n"
            "'¿Olvidaste tu contraseña?' para restablecerla por correo."
        )

    else:
        return (
            "No entendí tu mensaje.\n\n"
            "Puedes escribir palabras como:\n"
            "- hola\n- categorias\n- publicar\n- registro\n- reglas\n- ayuda"
        )

# =========================================
# FLASK APP
# =========================================
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    """Endpoint JSON — recibe mensaje y devuelve respuesta."""
    body    = request.get_json(force=True, silent=True) or {}
    mensaje = body.get("mensaje", "").strip()

    if not mensaje:
        return jsonify({"respuesta": "No recibí ningún mensaje. ¿Puedes escribir algo?"}), 400

    return jsonify({"respuesta": responder_mensaje(mensaje)})

@app.route("/webhook", methods=["POST"])
def webhook():
    """Webhook para Twilio / WhatsApp."""
    mensaje_entrante = request.values.get("Body", "")
    numero_remitente = request.values.get("From", "")

    print(f"Mensaje de {numero_remitente}: {mensaje_entrante}")

    respuesta_texto = responder_mensaje(mensaje_entrante)
    resp = MessagingResponse()
    resp.message(respuesta_texto)

    response = app.make_response(str(resp))
    response.headers["Content-Type"]               = "application/xml"
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

@app.route("/", methods=["GET"])
def inicio():
    return "Chatbot del Foro Estudiantil activo."

if __name__ == "__main__":
    print("\n🚀 Chatbot corriendo en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)