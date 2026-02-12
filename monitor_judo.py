import requests
import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def test_connection():
    # Mensagem de teste simples
    message = "🥋 TESTE DO TATAME RADAR: Se você recebeu isso, a conexão está OK!"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    
    print(f"Tentando enviar para o ID: {CHAT_ID}")
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ Sucesso! Verifique seu Telegram.")
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_connection()
