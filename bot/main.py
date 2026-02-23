import os
import json
import urllib.request
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN', '8447615128:AAEQAar0cg8FZohRFpRbGG3FusSS1hyN12s')
WEBHOOK_URL = 'https://quinta-avenida-pro-bot.vercel.app/'


def tg_post(method, payload):
    url = f'https://api.telegram.org/bot{TOKEN}/{method}'
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST'
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f'Error: {e}')
        return {'ok': False, 'error': str(e)}


def tg_get(method):
    url = f'https://api.telegram.org/bot{TOKEN}/{method}'
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def send_message(chat_id, text, reply_markup=None, parse_mode='Markdown', message_thread_id=None):
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
    if reply_markup:
        payload['reply_markup'] = reply_markup
    if message_thread_id:
        payload['message_thread_id'] = message_thread_id
    return tg_post('sendMessage', payload)


@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()
    if not update:
        return 'ok'
    thread_id = None
    if 'message' in update:
        msg = update['message']
        chat_id = msg['chat']['id']
        text = msg.get('text', '')
        thread_id = msg.get('message_thread_id', None)
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
                reply_markup=kb,
                message_thread_id=thread_id
            )
        elif text == '/menu':
            kb = {
                'inline_keyboard': [
                    [{'text': 'Ver Portafolio', 'callback_data': 'portfolio'}],
                    [{'text': 'Ver Planes', 'callback_data': 'plans'}]
                ]
            }
            send_message(chat_id, 'Menu principal:', reply_markup=kb, message_thread_id=thread_id)
        else:
            send_message(chat_id, f'Recibido: {text}\n\nUsa /start para el menu.', message_thread_id=thread_id)
    if 'callback_query' in update:
        cb = update['callback_query']
        chat_id = cb['message']['chat']['id']
        thread_id = cb['message'].get('message_thread_id', None)
        data = cb.get('data', '')
        msgs = {
            'portfolio': '*Portafolio*\n- Identidad visual\n- Social media\n- Campanas digitales',
            'plans': '*Plan $200/mes*\n- Gestion de marca\n- 4 sesiones estrategia\n- Contenido personalizado\n- Reportes KPIs',
            'pr_unido': '*Puerto Rico Unido*\nEcosistema Digital del Caribe\nMeta: $50-70M en 5 anos.',
            'contact': '*Contacto*\nEmail: info@barbosaagency.ai\nTelegram: @BarbosaAgencyAI'
        }
        if data in msgs:
            send_message(chat_id, msgs[data], message_thread_id=thread_id)
        tg_post('answerCallbackQuery', {'callback_query_id': cb['id']})
    return 'ok'


@app.route('/', methods=['GET'])
def index():
    return jsonify({'bot': 'Quinta Avenida Pro', 'status': 'online'})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'bot': 'Quinta Avenida Pro', 'status': 'healthy'})


@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    result = tg_post('setWebhook', {
        'url': WEBHOOK_URL,
        'allowed_updates': ['message', 'callback_query', 'channel_post', 'edited_message']
    })
    return jsonify(result)


@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    result = tg_post('deleteWebhook', {'drop_pending_updates': True})
    return jsonify(result)


@app.route('/webhook_info', methods=['GET'])
def webhook_info():
    result = tg_get('getWebhookInfo')
    return jsonify(result)


@app.route('/getme', methods=['GET'])
def getme():
    result = tg_get('getMe')
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8080)))
