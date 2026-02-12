import requests
from bs4 import BeautifulSoup
import os
import time

# Configurações do WhatsApp (serão pegas do GitHub Secrets)
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')  # Seu número com código do país (ex: 5521999999999)
API_KEY = os.environ.get('API_KEY')            # A chave que você pegou no passo 1

# Palavras-chave que indicam oportunidade ou brecha
KEYWORDS = [
    "seletiva", "edital", "aberta", "inscrição", "processo seletivo", 
    "campeonato brasileiro", "troféu brasil", "ranking", "regulamento", "judô", "judo", "rio"
]

def send_whatsapp_message(message):
    url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE_NUMBER}&text={message}&apikey={API_KEY}"
    try:
        requests.get(url)
        print("Mensagem enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def check_cbj():
    url = "https://cbj.com.br/noticias/"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ajuste conforme o layout do site da CBJ (geralmente títulos estão em h2, h3 ou a)
        # Este é um seletor genérico para pegar as manchetes recentes
        articles = soup.find_all('h3', limit=5) 
        
        found_news = []
        for article in articles:
            title = article.get_text().strip().lower()
            link = article.find_parent('a')['href'] if article.find_parent('a') else "Link não encontrado"
            
            for word in KEYWORDS:
                if word in title:
                    found_news.append(f"CBJ: {title.upper()} - {link}")
                    break
        return found_news
    except Exception as e:
        print(f"Erro ao acessar CBJ: {e}")
        return []

def check_fjerj():
    url = "https://fjerj.com.br/noticias/" # Exemplo, verificar URL exata
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('h2', limit=5) # FJERJ costuma usar h2 para títulos
        
        found_news = []
        for article in articles:
            title = article.get_text().strip().lower()
            # Tentar achar o link
            link_tag = article.find('a')
            link = link_tag['href'] if link_tag else "fjerj.com.br"
            
            for word in KEYWORDS:
                if word in title:
                    found_news.append(f"FJERJ: {title.upper()} - {link}")
                    break
        return found_news
    except Exception as e:
        print(f"Erro ao acessar FJERJ: {e}")
        return []

def main():
    print("Iniciando monitoramento...")
    alerts = []
    alerts.extend(check_cbj())
    alerts.extend(check_fjerj())
    
    if alerts:
        # Formata a mensagem para o WhatsApp (quebra de linha é %0A)
        msg_text = "ALERTA JUDÔ - OPORTUNIDADE:%0A" + "%0A".join(alerts)
        # Substitui espaços por + para URL
        msg_text = msg_text.replace(" ", "+")
        send_whatsapp_message(msg_text)
    else:
        print("Nenhuma oportunidade encontrada hoje com as palavras-chave.")

if __name__ == "__main__":

    main()
