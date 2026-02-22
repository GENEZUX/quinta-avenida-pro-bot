import os
import asyncio
import random
import logging
import json
import urllib.request
from flask import Flask, request, jsonify
from telegram import Bot, Update

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
OPENAI_API_KEY = os.environ.get('OPENAI_KEY', '')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '0'))

FRASES_PRO = [
    "Hagamos que el dinero trabaje para nosotros, no al reves.",
    "En la Quinta Avenida no aceptamos migajas. Vamos por el pastel completo.",
    "Negociar es un arte, y tu eres el pincel.",
    "Genesis MetaWorks no solo construye mundos, construye imperios.",
    "La mentalidad de escasez es para amateurs. Aqui somos Pros."
]

async def handle_update(data: dict):
    bot = Bot(token=TOKEN)
    async with bot:
        update = Update.de_json(data, bot)
        msg = update.message
        if not msg or not msg.text:
            return
        text = msg.text.strip()
        chat_id = msg.chat_id

        if text == '/start':
            respuesta = (
                "*QUINTA AVENIDA PRO BOT*\n"
                "Bienvenido al centro de mando de Genesis MetaWorks.\n"
                "Estoy listo para analizar ofertas y negociar como un tiburon de Wall Street.\n\n"
                "Comandos:\n"
                "/stats - Ver estadisticas\n"
                "/mercado - Analisis de mercado actual\n"
                "/frases - Motivacion Pro\n\n"
                "Enviame una oferta de trabajo para analizarla."
            )
            await bot.send_message(chat_id=chat_id, text=respuesta, parse_mode='Markdown')

        elif text == '/stats':
            await bot.send_message(
                chat_id=chat_id,
                text="*Estadisticas de la Semana:*\n- Ofertas analizadas: 12\n- Negociaciones exitosas: 8\n- ROI estimado: +25%",
                parse_mode='Markdown'
            )

        elif text == '/mercado':
            await bot.send_message(
                chat_id=chat_id,
                text="*Analisis de Mercado:* El sector de AI Automation esta en auge. Tarifas recomendadas: $50-$150/hr.",
                parse_mode='Markdown'
            )

        elif text == '/frases':
            await bot.send_message(
                chat_id=chat_id,
                text=f"*Frase Pro:* {random.choice(FRASES_PRO)}",
                parse_mode='Markdown'
            )

        elif not text.startswith('/'):
            await bot.send_message(chat_id=chat_id, text="Analizando oferta con mentalidad Quinta Avenida...")
            if not OPENAI_API_KEY or OPENAI_API_KEY.startswith('sk-placeholder'):
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"Oferta recibida: {text}\n\nEstandar NYC: $15-22/hr para CS bilingue. Si la oferta es menor a $15/hr, es inaceptable. Negocia al alza."
                )
                return
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Eres un experto negociador de la Quinta Avenida en Nueva York. Analiza la oferta y sugiere como pedir mas dinero o mejores condiciones de forma profesional pero agresiva. Estandar NYC CS bilingue: $15-22/hr."},
                        {"role": "user", "content": text}
                    ]
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"*Estrategia de Negociacion:*\n{response.choices[0].message.content}",
                    parse_mode='Markdown'
                )
            except Exception as e:
                await bot.send_message(chat_id=chat_id, text=f"Error analizando oferta: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        asyncio.run(handle_update(data))
        return jsonify({'ok': True})
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/set_webhook')
def set_webhook():
    try:
        webhook_url = 'https://quinta-avenida-pro-bot.vercel.app/webhook'
        api_url = f'https://api.telegram.org/bot{TOKEN}/setWebhook'
        payload = json.dumps({'url': webhook_url}).encode('utf-8')
        req = urllib.request.Request(api_url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

        @app.route('/getme')
def getme():
    try:
        api_url = f'https://api.telegram.org/bot{TOKEN}/getMe'
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))
        return jsonify(result)
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({'status': 'running', 'bot': 'Quinta Avenida Pro', 'version': '2.1'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'bot': 'Quinta Avenida Pro'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))