import requests
import csv
import time
from datetime import datetime

CLIENT_ID = 'Your ID'
CLIENT_SECRET = 'Your secret ID'
REALM_ID = 1390
FILENAME = "history_erp_auctions.csv"

def get_token():
    res = requests.post(
        "https://oauth.battle.net/token", 
        data={"grant_type": "client_credentials"}, 
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    return res.json().get("access_token") if res.status_code == 200 else None

def collect_and_save():
    token = get_token()
    if not token:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Erreur d'authentification.")
        return

    url = f"https://eu.api.blizzard.com/data/wow/connected-realm/{REALM_ID}/auctions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Battlenet-Namespace": "dynamic-eu",
        "User-Agent": "Mozilla/5.0"
    }
    
    res = requests.get(url, headers=headers)
    
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
                
        print(f"[{current_time}] Succès : {len(auctions)} transactions ajoutées à l'historique.")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Erreur API : {res.status_code}")

if __name__ == "__main__":
    print("--- Démarrage du collecteur automatique ---")
    
    while True:
        collect_and_save()
        time.sleep(3600)