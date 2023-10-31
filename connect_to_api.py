import requests
import keys

import json

import re

endpoint = "https://api.zotero.org"

def main():
    headers = {
            'Zotero-API-Version': str(3),
            'Zotero-API-Key': keys.API_KEY
            }

    parameters = {
                'format': 'keys',
                'itemType': 'attachment'
            }

    r = requests.get(f'{endpoint}/users/{keys.USER_ID}/items', headers=headers, params=parameters)
    item_keys = r.text.split('\n')[:-1]
    for item in item_keys:
        r = requests.get(f'{endpoint}/users/{keys.USER_ID}/items/{item}', headers=headers)
        ob = json.loads(r.text)
        print(ob)
        #if 'extra' in ob['data']:
        #    expression = "Citation Key: ([a-zA-Z0-9_]+)"
        #    print(item, re.search(expression, ob['data']['extra']).group(1))

if __name__=="__main__":
    main()

