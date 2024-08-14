import requests
import json
import pandas as pd




headers  = {
    'user_agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'Referer':'https://statsroyale.com/',
}



def get_img_url():
    with open('gamedata.json','r') as f:
        game_data = json.load(f)
    for data in game_data['items']['spells']:
        url =  f'https://cdn.statsroyale.com/v6/cards/small_b/{data["id"]}.webp'
        response  =  requests.get(url,timeout=5,headers=headers)
        # 保存图片
        with open(f'./img/{data["name"]}.webp','ab') as b:
            b.write(response.content)
        

    
if __name__ == '__main__':
    get_img_url()

