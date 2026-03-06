import requests
from bs4 import BeautifulSoup
import time
import json

# --- CONFIGURAÇÕES BOT TELEGRAM ---
TOKEN = "xxx" #<-- Aqui sera inserido o Token do Bot do Telegram
CHAT_ID = "xxx" #<-- Aqui sera inserido o Chat ID do grupo que ira receber as mensagens

def enviar_telegram(mensagem):
    url_api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem}
    try:
        requests.post(url_api, data=payload)
    except Exception as e:
        print(f"Erro no Telegram: {e}")

def extrair_preco(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        inteiro = soup.find("span", class_="a-price-whole")
        if inteiro:
            valor = inteiro.get_text().replace(".", "").replace(",", "")
            return float(valor)
    except:
        return None
    return None

def monitorar_todos():
    # Lendo o arquivo JSON
    with open('produtos.json', 'r') as f:
        lista_produtos = json.load(f)

    print(f"\n--- Iniciando verificação às {time.strftime('%H:%M:%S')} ---")

    for item in lista_produtos:
        preco_atual = extrair_preco(item['url'])
        
        if preco_atual:
            print(f"ID: {item['nome']} | Preço: R$ {preco_atual:.2f}")
            
            # Comparando com o alvo do JSON
            if preco_atual <= item['alvo']:
                msg = f"🚨 BAIXOU! {item['nome']} está R$ {preco_atual:.2f}\nLink: {item['url']}"
                enviar_telegram(msg)
        else:
            print(f"⚠️ Não foi possível obter o preço de: {item['nome']}")

if __name__ == "__main__":
    while True:
        monitorar_todos()
        print("Aguardando 1 hora para a próxima verificação...")
        time.sleep(30)