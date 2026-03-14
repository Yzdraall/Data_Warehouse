import re

#fichiers d'entrée et de sortie
FILE_IN = 'AuctionDB.lua'
FILE_AUCTIONS = 'auctions_from_lua.csv'
FILE_ITEMS = 'items_from_lua.csv'

print("--- Transformation du fichier Lua en CSV ---")

#génération de auctions.csv
print("1. Génération des transactions (auctions.csv)...")
with open(FILE_IN, 'r', encoding='utf-8', errors='ignore') as file, open(FILE_AUCTIONS, 'w', encoding='utf-8') as out_file:
    out_file.write("scan_time,item_id,modifier,player,duration,quantity,min_bid,buyout\n")
    elapsed = ''
    
    for line in file:
        if '["elapsed"]' in line:
            elapsed = line.split('=')[1].strip().strip('",')
        
        if '["data"]' in line:
            line = line.split('=')[1].strip().strip('",')
            line = re.sub(r'(\d) i', r'\1, i', line)
            data = line.split(", i")
            
            for item_data in data:
                if not item_data: continue
                parts = item_data.split("!")
                item_full = parts[0]
                item_id = item_full.split("?")[0]
                modifier = item_full.split("?")[1] if "?" in item_full else ""
                
                for p in parts[1:]:
                    player_parts = p.split("/")
                    if len(player_parts) < 2: continue
                    player = player_parts[0]
                    auctions = player_parts[1].split("&")
                    
                    for a in auctions:
                        a = a.strip(',"')
                        a_parts = a.split(",")
                        if len(a_parts) >= 5:
                            clean_a = f"{a_parts[0]},{a_parts[1]},{a_parts[2]},{a_parts[4]}"
                            out_file.write(f"{elapsed},{item_id},{modifier},{player},{clean_a}\n")

#génération de items_from_lua.csv
print("2. Génération du référentiel (items.csv)...")
with open(FILE_IN, 'r', encoding='utf-8', errors='ignore') as file, open(FILE_ITEMS, 'w', encoding='utf-8') as out_file:
    out_file.write("item_id,modifier,name,url\n")
    read = True
    
    for line in file:
        if '["itemDB_2"]' in line:
            read = False
            
        if not read and "Hitem:" in line:
            item_num = re.search(r'Hitem:(\d+):', line)
            item_mod = re.search(r'\?(\d+)"\]', line)
            item_desc = re.search(r'\|h\[(.*?)\]\|h', line)
            
            if item_num and item_desc:
                i_id = item_num.group(1)
                i_mod = item_mod.group(1) if item_mod else ""
                i_name = item_desc.group(1)
                i_url = f"https://classic.wowhead.com/item={i_id}"
                
                out_file.write(f"{i_id},{i_mod},{i_name},{i_url}\n")

print("Success CSV file created")