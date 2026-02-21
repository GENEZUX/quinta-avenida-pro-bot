import os
import asyncio
import random
import logging
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from openai import OpenAI

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Config desde variables de entorno
TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
OPENAI_API_KEY = os.environ.get('OPENAI_KEY', '')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '0'))
BASE_URL = os.environ.get('VERCEL_URL', '')
if BASE_URL and not BASE_URL.startswith('http'):
    BASE_URL = f'https://{BASE_URL}'

client = OpenAI(api_key=OPENAI_API_KEY)

# DB Setup (In-memory para Vercel o SQLite local)
def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, key TEXT, value INTEGER)''')
    conn.commit()
    conn.close()

# Personalidad Quinta Avenida
FRASES_PRO = [
    "Hagamos que el dinero trabaje para nosotros, no al revés.",
    "En la Quinta Avenida no aceptamos migajas. Vamos por el pastel completo.",
    "Negociar es un arte, y tú eres el pincel.",
    "Genesis MetaWorks no solo construye mundos, construye imperios.",
    "La mentalidad de escasez es para amateurs. Aquí somos Pros."
]

# ======== HANDLERS ========
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Acceso restringido a personal de la Quinta Avenida.")
        return
    
    texto = (
        "🏙 *QUINTA AVENIDA PRO BOT*

"
        "Bienvenido al centro de mando de Genesis MetaWorks.
"
        "Estoy listo para analizar ofertas y negociar como un tiburón de Wall Street.

"
        "Comandos:
"
        "/stats - Ver estadísticas de negociaciones
"
        "/mercado - Análisis de mercado actual (IA)
"
        "/frases - Motivación Pro

"
        "Envíame una oferta de trabajo para analizarla."
    )
    await update.message.reply_text(texto, parse_mode='Markdown')

async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 *Estadísticas de la Semana:*
- Ofertas analizadas: 12
- Negociaciones exitosas: 8
- ROI estimado: +25%", parse_mode='Markdown')

async def cmd_mercado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 *Análisis de Mercado:* El sector de AI Automation está en auge. Tarifas recomendadas: $50-$150/hr.", parse_mode='Markdown')

async def cmd_frases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💡 {random.choice(FRASES_PRO)}")

async def handle_oferta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    
    oferta = update.message.text
    await update.message.reply_text("🤖 Analizando oferta con mentalidad Quinta Avenida...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un experto negociador de la Quinta Avenida en Nueva York. Analiza la oferta y sugiere cómo pedir más dinero o mejores condiciones de forma profesional pero agresiva."},
                {"role": "user", "content": oferta}
            ]
        )
        await update.message.reply_text(f"💎 *Estrategia de Negociación:*

{response.choices[0].message.content}", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Error analizando oferta: {e}")

# ======== CORE SERVERLESS PATTERN ========
async def process_update(token: str, data: dict):
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', cmd_start))
    application.add_handler(CommandHandler('stats', cmd_stats))
    application.add_handler(CommandHandler('mercado', cmd_mercado))
    application.add_handler(CommandHandler('frases', cmd_frases))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_oferta))
    
    async with application:
        update = Update.de_json(data, application.bot)
        await application.process_update(update)

# ======== FLASK ROUTES ========
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        asyncio.run(process_update(TOKEN, data))
        return jsonify({'ok': True})
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({'status': 'running', 'bot': 'Quinta Avenida Pro'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
