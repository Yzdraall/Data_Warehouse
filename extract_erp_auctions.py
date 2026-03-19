import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLIZZARD_CLIENT_SECRET')

print("--- Extraction de l'Hôtel des Ventes ---")

#recup du token
res_token = requests.post(
    "https://oauth.battle.net/token", 
    data={"grant_type": "client_credentials"}, 
    auth=(CLIENT_ID, CLIENT_SECRET)
)
token = res_token.json().get("access_token")

if not token:
    print("Échec de l'authentification.")
    exit()

print("Token obtenu. Contournement du pare-feu...")

#requête vers le serveur Hyjal fr
url = "https://eu.api.blizzard.com/data/wow/connected-realm/1390/auctions"

#User-Agent de navigateur et Auth en Header
headers = {
    "Authorization": f"Bearer {token}",
    "Battlenet-Namespace": "dynamic-eu",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

res = requests.get(url, headers=headers)

if res.status_code == 200:
    auctions = res.json().get("auctions", [])
    
    #save
    with open("source_erp_wow_auctions.json", "w", encoding="utf-8") as f:
        json.dump(auctions, f, ensure_ascii=False, indent=4)
        
    print(f"Succes ! {len(auctions)} annonces téléchargées avec succès.")
else:
    print(f"Blocage persistant (Code {res.status_code}) : {res.text}")