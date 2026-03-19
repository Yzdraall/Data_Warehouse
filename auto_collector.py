import requests
import csv
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLIZZARD_CLIENT_SECRET')
REALM_ID = 1390 # Serveur Hyjal
FILENAME = "history_erp_auctions.csv"

def get_token():
    try:
        res = requests.post(
            "https://oauth.battle.net/token", 
            data={"grant_type": "client_credentials"}, 
            auth=(CLIENT_ID, CLIENT_SECRET),
            timeout=10
        )
        return res.json().get("access_token") if res.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Erreur réseau lors de l'authentification : {e}")
        return None

def collect_and_save():
    token = get_token()
    if not token:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Impossible de récupérer le Token. Annulation de la collecte de cette heure.")
        return

    url = f"https://eu.api.blizzard.com/data/wow/connected-realm/{REALM_ID}/auctions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Battlenet-Namespace": "dynamic-eu",
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        
        if res.status_code == 200:
            auctions = res.json().get("auctions", [])
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(FILENAME, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if f.tell() == 0:
                    writer.writerow(["scan_time", "auction_id", "item_id", "quantity", "unit_price", "time_left"])
                
                for auc in auctions:
                    writer.writerow([
                        current_time,
                        auc.get("id", ""),
                        auc.get("item", {}).get("id", ""),
                        auc.get("quantity", ""),
                        auc.get("unit_price", auc.get("buyout", "")),
                        auc.get("time_left", "")
                    ])
                    
            print(f"[{current_time}] Succès : {len(auctions)} transactions ajoutées.")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erreur API : Code {res.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Erreur réseau lors du téléchargement : {e}")

if __name__ == "__main__":
    print("--- Démarrage du collecteur automatique (Mode Résilient) ---")
    print("Le script va récupérer les données toutes les heures. (CTRL+C pour arrêter)")
    
    while True:
        collect_and_save()
        # Pause de 3600 secondes avant le prochain appel
        time.sleep(3600)