import requests
import keys

import json

import re

from database import create_all_tables, Item, Attachment, LibraryVersion

import os

endpoint = "https://api.zotero.org"

def main():

    create_all_tables()
    headers = {
            'Zotero-API-Version': str(3),
            'Zotero-API-Key': keys.API_KEY
            }

    parameters = {
                'format': 'keys',
                'itemType': '-attachment'
            }

    r = requests.get(f'{endpoint}/users/{keys.USER_ID}/items', headers=headers, params=parameters)
    item_keys = r.text.split('\n')[:-1]

    last_synced_version = 0
    for previous_version in LibraryVersion.select().where(LibraryVersion.attachments_up_to_date==True).order_by(LibraryVersion.version.desc()):
        last_synced_version = previous_version.version
        break
    
    last_modified_version = int(r.headers['Last-Modified-Version'])
    version = LibraryVersion.get_or_create(version= last_modified_version)[0]
    if version.items_up_to_date:
        return

    number_of_items = len(item_keys)
    for i, item in enumerate(item_keys):
        print(f'item {i} out of {number_of_items}')
        r = requests.get(f'{endpoint}/users/{keys.USER_ID}/items/{item}', headers=headers)
        ob = json.loads(r.text)

        item_version = int(ob['version'])
        if item_version < last_synced_version:
            break 

        if 'extra' in ob['data']:
            expression = "Citation Key: ([a-zA-Z0-9_]+)" 
            result = re.search(expression, ob['data']['extra'])
            if result is not None:
                try:
                    saved_item = Item.get(zotero_id = item)
                except Item.DoesNotExist:
                    saved_item = Item(zotero_id = item)
                saved_item = Item.get_or_create(zotero_id=item)
                saved_item.version = item_version
                saved_item.citation_key = result.group(1)
                saved_item.save()

   
 
    version.items_up_to_date = True
    version.save()


                

if __name__=="__main__":
    main()

