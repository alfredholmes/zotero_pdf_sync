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
    version = LibraryVersion.get_or_create(version= last_modified_version)[0]
    if version.attachments_up_to_date:
        return


    last_synced_version = 0
    for previous_version in LibraryVersion.select().where(LibraryVersion.attachments_up_to_date==True).order_by(LibraryVersion.version.desc()):
        last_synced_version = previous_version.version
        break

    
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

        if ob['version'] < last_synced_version:
            break

        try:
            if 'path' in ob and 'parentItem' in ob:
                parent_item = Item.get(zotero_id=ob['parentItem'])
                try:
                    attachment = Attachment.get(zotero_id=item) 
                except Attachment.DoesNotExist:
                    attachment = Attachment(zotero_id=item)
                attachment.item = parent_item
                attachment.path = ob['path']
                attachment.version = ob['version']
                attachment.save()
            #print(parent_item.citation_key, ob['path'])
        except Item.DoesNotExist:
            print(f'no item with id {ob["parentItem"]}')

    for attachment in Attachment: 
        if attachment.zotero_id not in item_keys:
            attachment.delete_instance()

    version.attachments_up_to_date = True
    version.save()


                

if __name__=="__main__":
    main()

