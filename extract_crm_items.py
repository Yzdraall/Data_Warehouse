import requests
import json
import csv
from collections import Counter

CLIENT_ID = 'Your ID'
CLIENT_SECRET = 'Your secret ID'

print("--- Création du Référentiel Objets (CRM) ---")

#logging in
res_token = requests.post(
    "https://oauth.battle.net/token", 
    data={"grant_type": "client_credentials"}, 
    auth=(CLIENT_ID, CLIENT_SECRET)
)
token = res_token.json().get("access_token")

if not token:
    print("Échec de l'authentification.")
    exit()

#on lit l'erp 
try:
    with open("source_erp_wow_auctions.json", 'r', encoding='utf-8') as f:
        auctions = json.load(f)
except FileNotFoundError:
    print("Fichier source_erp_wow_auctions.json introuvable.")
    exit()

#extraction des 500 objets les plus vendus pour le dictionnaire
item_ids = [auc["item"]["id"] for auc in auctions]
top_items = [item[0] for item in Counter(item_ids).most_common(500)]
print(f"{len(set(item_ids))} objets uniques identifiés. Traduction des 500 plus populaires...")

#on interroge l'api avec les headers sécurisés
headers = {
    "Authorization": f"Bearer {token}",
    "Battlenet-Namespace": "static-eu",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

extracted_items = []
for item_id in top_items:
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
        extracted_items.append(info)
        print(f"  + {info['Name']}")

#csv save
with open("source_crm_items.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["ID", "Name", "Quality", "ItemClass"])
    writer.writeheader()
    writer.writerows(extracted_items)
    
print(f"\nSuccès : {len(extracted_items)} objets sauvegardés dans source_crm_items.csv.")