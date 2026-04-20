import pickle
import random

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ── Token de BotFather ─────────────────────────────────
TOKEN = "" #aqui va el token del bot de Telegram, que se obtiene al crear el bot con BotFather. Es importante mantenerlo privado.

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

UMBRAL_CONFIANZA = 0.30

# ── Función principal de respuesta (sin cambios) ───────
def obtener_respuesta(mensaje: str) -> str:
    texto = mensaje.lower().strip()

    if not texto:
        return "Por favor escribe algo para poder ayudarte."

    tag          = pipeline.predict([texto])[0]
    probabilidad = pipeline.predict_proba([texto]).max()

    if probabilidad < UMBRAL_CONFIANZA:
        tag = "desconocido"

    opciones = respuestas.get(tag, respuestas.get("desconocido", ["No entiendo lo que dices."]))
    return random.choice(opciones)

# ── Handlers de Telegram ───────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    await update.message.reply_text(
        f"¡Hola {nombre}! 👋 Soy el Asistente del Foro Estudiantil.\n\n"
        "Escríbeme cualquier duda sobre el foro y te ayudo."
    )

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje   = update.message.text
    respuesta = obtener_respuesta(mensaje)
    await update.message.reply_text(respuesta)

# ── Ejecución ──────────────────────────────────────────
if __name__ == "__main__":
    print("Bot de Telegram iniciado.")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    app.run_polling()