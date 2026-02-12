import requests
from bs4 import BeautifulSoup
import os

# Puxa as chaves que você configurou no GitHub Secrets
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# Suas palavras-chave de monitoramento
KEYWORDS = [
    "seletiva", "edital", "aberta", "inscrição", "vaga", "convocação", "chamada pública", "fomento", "incentivo"
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Erro ao enviar: {e}")

def check_site(url, site_name):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # O Radar agora varre TUDO que for texto clicável (links)
        links = soup.find_all('a')
        
        found = []
        seen_titles = set()

        for link in links:
            text = link.get_text().strip().lower()
            href = link.get('href', '')
            
            # Se o texto do link tiver uma das palavras-chave
            if any(word in text for word in KEYWORDS):
                if text not in seen_titles and len(text) > 10:
                    full_url = href if href.startswith('http') else url + href
                    found.append(f"🥋 *{site_name}*: {text.upper()}\n🔗 {full_url}")
                    seen_titles.add(text)
        
        return found[:5] # Pega as 5 notícias mais recentes para não lotar o chat
    except Exception as e:
        print(f"Erro no site {site_name}: {e}")
        return []

def main():
    print("TatameRadar iniciando ronda...")
    results = []
    
    # Sites da Confederação e da Federação Estadual
    results.extend(check_site("https://cbj.com.br/noticias/", "CBJ"))
    results.extend(check_site("https://fjerj.com.br/noticias/", "FJERJ"))
    
    if results:
        # Envia cada notícia encontrada para o seu irmão não perder nada
        full_message = "🛰️ *TATAME RADAR IDENTIFICOU:* \n\n" + "\n\n".join(results)
        send_telegram_message(full_message)
    else:
        print("Nada relevante hoje.")

if __name__ == "__main__":
    main()

