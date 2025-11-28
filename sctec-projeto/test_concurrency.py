import requests
import threading
import time

# URL do serviço Flask (Cérebro)
BASE_URL = "http://localhost:5000"

# Parâmetros do teste
NUM_REQUESTS = 10
TARGET_TIME_SLOT = "2025-12-01T05:00:00Z"
CLIENT_IDS = range(1, NUM_REQUESTS + 1)

def send_scheduling_request(client_id):
    """
    Simula um cientista tentando agendar o mesmo slot de tempo.
    """
    url = f"{BASE_URL}/agendamentos"
    payload = {
        "cientista_id": client_id,
        "horario_inicio_utc": TARGET_TIME_SLOT
    }
    
    try:
        print(f"[Cientista {client_id}] ⏳ Tentando agendar...")
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 201:
            print(f"[Cientista {client_id}] ✅ SUCESSO! Agendamento criado. ID: {response.json().get('id')}")
        elif response.status_code == 409:
            print(f"[Cientista {client_id}] ❌ CONFLITO! {response.json().get('message')}")
        else:
            print(f"[Cientista {client_id}] ❓ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"[Cientista {client_id}] 🚨 ERRO: {e}")

if __name__ == "__main__":
    print(f"--- 🧪 Iniciando Teste de Concorrência (Exclusão Mútua) ---")
    print(f"Disparando {NUM_REQUESTS} requisições simultâneas para o horário {TARGET_TIME_SLOT}...\n")
    
    threads = []
    for i in CLIENT_IDS:
        t = threading.Thread(target=send_scheduling_request, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(0.05) # Pequeno intervalo para garantir ordem de chegada no log visual

    for t in threads:
        t.join()

    print("\n--- 🏁 Teste Finalizado ---")