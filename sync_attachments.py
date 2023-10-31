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
                'itemType': 'attachment'
            }

    r = requests.get(f'{endpoint}/users/{keys.USER_ID}/items', headers=headers, params=parameters)

    last_modified_version = int(r.headers['Last-Modified-Version'])
    version = LibraryVersion.get_or_create(version= last_modified_version)
    if not version[0]:
        return

    
    item_keys = r.text.split('\n')[:-1]

    item_objects = []

    number_of_items = len(item_keys)
    for i, item in enumerate(item_keys):
        try:
            Attachment.get(zotero_id = item)
            continue
        except Attachment.DoesNotExist:
            pass
        print(f'item {i} out of {number_of_items}')
        r = requests.get(f'{endpoint}/users/{keys.USER_ID}/items/{item}', headers=headers)
        ob = json.loads(r.text)['data']

        print(ob)



        try:
            if 'path' in ob and 'parentItem' in ob:
                parent_item = Item.get(zotero_id=ob['parentItem'])
                attachment = Attachment.get_or_create(zotero_id=item, item=parent_item, path=ob['path'], version=ob['version'])
            #print(parent_item.citation_key, ob['path'])
        except Item.DoesNotExist:
            print(f'no item with id {ob["parentItem"]}')

    for attachment in Attachment: 
        if attachment.zotero_id not in items_keys:
            attachment.delete_instance()




                

if __name__=="__main__":
    main()
