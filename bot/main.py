import os
import json
import urllib.request
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN', '8116584281:AAFrf7l-Q48H09VjL36-j8T88C22Xz-G7Ww')
WEBHOOK_URL = 'https://quinta-avenida-pro-bot.vercel.app/'


def send_message(chat_id, text, reply_markup=None, parse_mode='Markdown'):
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
    if reply_markup:
        data['reply_markup'] = reply_markup
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(
        url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST'
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f'Error: {e}')
        return None


@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()
    if not update:
        return 'ok'
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        if text == '/start':
            keyboard = {
                'inline_keyboard': [
                    [{'text': 'Portafolio de Marca', 'callback_data': 'portfolio'}],
                    [{'text': 'Planes de Servicio $200/mes', 'callback_data': 'plans'}],
                    [{'text': 'Puerto Rico Unido', 'callback_data': 'pr_unido'}],
                    [{'text': 'Contactar Agencia', 'callback_data': 'contact'}]
                ]
            }
            send_message(
                chat_id,
                '*Quinta Avenida Pro - Asistente Inteligente*

Bienvenida al sistema de gestion de marca premium de Barbosa Agency.ai

Selecciona una opcion:',
                reply_markup=keyboard
            )
        elif text == '/menu':
            keyboard = {
                'inline_keyboard': [
                    [{'text': 'Ver Portafolio', 'callback_data': 'portfolio'}],
                    [{'text': 'Ver Planes', 'callback_data': 'plans'}]
                ]
            }
            send_message(chat_id, 'Menu principal:', reply_markup=keyboard)
        else:
            send_message(chat_id, f'Recibido: {text}

Usa /start para ver el menu completo.')
    if 'callback_query' in update:
        callback = update['callback_query']
        chat_id = callback['message']['chat']['id']
        data = callback['data']
        if data == 'portfolio':
            send_message(chat_id, '*Portafolio de Marca*

Servicios:
- Identidad visual premium
- Estrategia de contenido
- Social media management
- Campanas digitales

Contacta para ver ejemplos de trabajo.')
        elif data == 'plans':
            send_message(chat_id, '*Plan Barbosa Agency $200/mes*

Incluyendo:
- Gestion de marca completa
- 4 sesiones mensuales de estrategia
- Contenido digital personalizado
- Reportes mensuales de KPIs
- Acceso a IA Quinta Avenida Pro

Contacta para iniciar: @BarbosaAgencyAI')
        elif data == 'pr_unido':
            send_message(chat_id, '*Puerto Rico Unido*

Ecosistema Digital del Caribe - Barbosa Agency.ai

Vision: Conectar empresas puertorriquenas con tecnologia de vanguardia AI para competir globalmente.

Meta: $50-70M valor empresa en 5 anos.')
        elif data == 'contact':
            send_message(chat_id, '*Contactar Barbosa Agency*

Email: info@barbosaagency.ai
Telegram: @BarbosaAgencyAI
Web: barbosaagency.ai

Especializados en:
- Branding con IA
- Automatizacion de marketing
- Puerto Rico mercado hispanohablante')
    return 'ok'


@app.route('/', methods=['GET'])
def index():
    return jsonify({'bot': 'Quinta Avenida Pro', 'status': 'online', 'agency': 'Barbosa Agency.ai'})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'bot': 'Quinta Avenida Pro', 'status': 'healthy'})


@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    url = f'https://api.telegram.org/bot{TOKEN}/setWebhook'
    data = {'url': WEBHOOK_URL}
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(
        url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST'
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            return jsonify(result)
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/getme', methods=['GET'])
def getme():
    url = f'https://api.telegram.org/bot{TOKEN}/getMe'
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            return jsonify(result)
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8080)))
