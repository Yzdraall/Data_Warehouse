import requests
import json
import csv
import os
import time
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLIZZARD_CLIENT_SECRET')



res_token = requests.post(
    "https://oauth.battle.net/token", 
    data={"grant_type": "client_credentials"}, 
    auth=(CLIENT_ID, CLIENT_SECRET)
)
token = res_token.json().get("access_token")

if not token:
    print("Authentification Failed.")
    exit()


known_items = set()
try:
    with open("source_crm_items.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            known_items.add(int(row["ID"]))
    print(f"[{len(known_items)}] already in crm.")
except FileNotFoundError:
    print("source_crm_items.csv file not found, it will be created.")


erp_items = set()
try:
    with open("history_erp_auctions.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("item_id") and row["item_id"].strip().isdigit():
                erp_items.add(int(row["item_id"]))
    print(f"[{len(erp_items)}] in erp.")
except FileNotFoundError:
    print("history_erp_auctions.csv file not found.")
    exit()


missing_ids = list(erp_items - known_items)
print(f"-> {len(missing_ids)} downloading missing objects...")

if not missing_ids:
    print("CRM up to date")
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

print(f"\nSuccess, source_crm_items.csv updated with {len(missing_ids)} new objects.")