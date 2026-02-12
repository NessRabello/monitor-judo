import requests
from bs4 import BeautifulSoup
import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# Focado em Oportunidades de Competição e de Verbas para a ONG
KEYWORDS = [
    "seletiva", "edital", "aberta", "inscrição", "regulamento", 
    "chamamento", "fomento", "incentivo", "vaga", "convocação"
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True}
    requests.post(url, data=payload)

def scan_site(url, site_name):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        found = []
        # Varre links e títulos atrás de oportunidades
        for el in soup.find_all(['a', 'h2', 'h3']):
            text = el.get_text().strip().lower()
            if any(word in text for word in KEYWORDS):
                link_tag = el if el.name == 'a' else el.find_parent('a')
                href = link_tag.get('href', '') if link_tag else url
                
                if len(text) > 10:
                    full_url = href if href.startswith('http') else url.split('.br')[0] + ".br" + href
                    entry = f"🚀 *{site_name}*: {text.upper()}\n🔗 {full_url}"
                    if entry not in found:
                        found.append(entry)
        return found[:3]
    except:
        return []

def main():
    all_alerts = []
    
    # Lista de alvos: Judô + Recursos Governamentais
    targets = [
        ("https://cbj.com.br/noticias/", "CBJ Notícias"),
        ("https://fjerj.com.br/boletins/", "FJERJ Boletins"),
        ("http://www.esporte.rj.gov.br/", "Secretaria Esporte RJ"), # Lei de Incentivo e editais estaduais
        ("https://www.gov.br/esporte/pt-br/noticias", "Ministério do Esporte"), # Verbas federais e Bolsa Atleta
    ]
    
    for url, name in targets:
        print(f"Limpando a área em {name}...")
        all_alerts.extend(scan_site(url, name))
    
    if all_alerts:
        msg = "🛰️ *TATAME RADAR: RELATÓRIO DE OPORTUNIDADES*\n\n" + "\n\n".join(all_alerts)
        send_telegram_message(msg)
    else:
        # Avisa que o bot está vivo, mas sem novidades críticas
        send_telegram_message("📡 *TatameRadar*: Ronda concluída. Nenhuma seletiva ou edital de fomento novo hoje.")

if __name__ == "__main__":
    main()
