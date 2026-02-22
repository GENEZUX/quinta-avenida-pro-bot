import os
import json
import urllib.request
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN', '8116584281:AAFrf7l-Q48H09VjL36-j8T88C22Xz-G7Ww')
WEBHOOK_URL = 'https://quinta-avenida-pro-bot.vercel.app/'


def send_message(chat_id, text, reply_markup=None, parse_mode='Markdown'):
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
    if reply_markup:
        payload['reply_markup'] = reply_markup
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST'
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f'Error: {e}')
        return None


def tg_get(method):
    url = f'https://api.telegram.org/bot{TOKEN}/{method}'
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {'ok': False, 'error': str(e)}


@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()
    if not update:
        return 'ok'
    if 'message' in update:
        msg = update['message']
        chat_id = msg['chat']['id']
        text = msg.get('text', '')
        if text == '/start':
            kb = {
                'inline_keyboard': [
                    [{'text': 'Portafolio de Marca', 'callback_data': 'portfolio'}],
                    [{'text': 'Planes $200/mes', 'callback_data': 'plans'}],
                    [{'text': 'Puerto Rico Unido', 'callback_data': 'pr_unido'}],
                    [{'text': 'Contactar Agencia', 'callback_data': 'contact'}]
                ]
            }
            send_message(
                chat_id,
                '*Quinta Avenida Pro*\n\nBienvenida a Barbosa Agency.ai\n\nSelecciona una opcion:',
                reply_markup=kb
            )
        elif text == '/menu':
            kb = {
                'inline_keyboard': [
                    [{'text': 'Ver Portafolio', 'callback_data': 'portfolio'}],
                    [{'text': 'Ver Planes', 'callback_data': 'plans'}]
                ]
            }
            send_message(chat_id, 'Menu principal:', reply_markup=kb)
        else:
            send_message(chat_id, f'Recibido: {text}\n\nUsa /start para el menu.')
    if 'callback_query' in update:
        cb = update['callback_query']
        chat_id = cb['message']['chat']['id']
        data = cb.get('data', '')
        msgs = {
            'portfolio': '*Portafolio*\n- Identidad visual\n- Social media\n- Campanas digitales',
            'plans': '*Plan $200/mes*\n- Gestion de marca\n- 4 sesiones estrategia\n- Contenido personalizado\n- Reportes KPIs',
            'pr_unido': '*Puerto Rico Unido*\nEcosistema Digital del Caribe\nMeta: $50-70M en 5 anos.',
            'contact': '*Contacto*\nEmail: info@barbosaagency.ai\nTelegram: @BarbosaAgencyAI'
        }
        if data in msgs:
            send_message(chat_id, msgs[data])
    return 'ok'


@app.route('/', methods=['GET'])
def index():
    return jsonify({'bot': 'Quinta Avenida Pro', 'status': 'online'})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'bot': 'Quinta Avenida Pro', 'status': 'healthy'})


@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    url = f'https://api.telegram.org/bot{TOKEN}/setWebhook'
    payload = {'url': WEBHOOK_URL}
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST'
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return jsonify(json.loads(resp.read().decode()))
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/getme', methods=['GET'])
def getme():
    result = tg_get('getMe')
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8080)))
