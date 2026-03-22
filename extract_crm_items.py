import requests
import json
import csv
import os
import time
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLIZZARD_CLIENT_SECRET')

print("--- Synchronisation Automatique du Référentiel Objets (CRM) ---")


res_token = requests.post(
    "https://oauth.battle.net/token", 
    data={"grant_type": "client_credentials"}, 
    auth=(CLIENT_ID, CLIENT_SECRET)
)
token = res_token.json().get("access_token")

if not token:
    print("Échec de l'authentification.")
    exit()


known_items = set()
try:
    with open("source_crm_items.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            known_items.add(int(row["ID"]))
    print(f"[{len(known_items)}] objets déjà présents dans source_crm_items.csv.")
except FileNotFoundError:
    print("Fichier source_crm_items.csv introuvable, il sera créé.")


erp_items = set()
try:
    with open("source_erp_wow_auctions.json", 'r', encoding='utf-8') as f:
        auctions = json.load(f)
        for auc in auctions:
            erp_items.add(int(auc["item"]["id"]))
    print(f"[{len(erp_items)}] objets uniques trouvés dans source_erp_wow_auctions.json.")
except FileNotFoundError:
    print("Fichier source_erp_wow_auctions.json introuvable.")
    exit()


missing_ids = list(erp_items - known_items)
print(f"-> {len(missing_ids)} nouveaux objets à télécharger depuis l'API Blizzard...")

if not missing_ids:
    print("Ton dictionnaire (CRM) est déjà parfaitement à jour !")
    exit()


headers = {
    "Authorization": f"Bearer {token}",
    "Battlenet-Namespace": "static-eu"
}


with open("source_crm_items.csv", 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["ID", "Name", "Quality", "ItemClass"])
    
    
    if len(known_items) == 0:
        writer.writeheader()

    for index, item_id in enumerate(missing_ids):
        url = f"https://eu.api.blizzard.com/data/wow/item/{item_id}?locale=fr_FR"
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            data = res.json()
            info = {
                "ID": item_id,
                "Name": data.get("name", "Inconnu"),
                "Quality": data.get("quality", {}).get("name", "Commune"),
                "ItemClass": data.get("item_class", {}).get("name", "Autre")
            }
            writer.writerow(info)
        
        time.sleep(0.05) 

print(f"\nSuccès : Le fichier source_crm_items.csv a été mis à jour avec {len(missing_ids)} nouveaux objets.")