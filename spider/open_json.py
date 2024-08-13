import json
import pandas as pd
df = pd.DataFrame()
with open('gamedata.json','r') as f:
    game_data = json.load(f)
    for data in game_data['items']['spells']:
        print(data['id'],data['name'])
        df['id'] = data['id']
        df['name'] = data['name']
