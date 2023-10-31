import requests
import keys

import json

import re
from list_files import get_files
from database import Item, Attachment

endpoint = "https://api.zotero.org"

def main():
    headers = {
            'Zotero-API-Version': str(3),
            'Zotero-API-Key': keys.API_KEY
            }

    parameters = {
                'format': 'keys',
                'itemType': '-attachment'
            }

    item = 'J4SUWDYA'

    #r = requests.get(f'{endpoint}/users/{keys.USER_ID}/items/{item}', headers=headers)
    #print(r.text)


    r = requests.get(f'{endpoint}/items/new?itemType=attachment&linkMode=linked_file')
    attachment = json.loads(r.text)

    parent_items = [item for item in Item]
    files = get_files(keys.PDF_DIRECTORY)

    
    for file in files:
        for item in parent_items:
            if item.citation_key in str(file):
                print(str(file), item.citation_key)
                path = 'attachments:' + str(file).split(keys.ZOTERO_ROOT)[1]
                attachment['path'] = path
                attachment['title'] = str(file).split('/')[-1]
                attachment['parentItem'] = item.zotero_id

                r = requests.post(f'{endpoint}/users/{keys.USER_ID}/items', data=json.dumps([attachment]),headers=headers)
                if r.status_code == 200:
                    #write succesfull
                    for completed in json.loads(r.text)['successful']:
                        Attachment.create(zotero_id = completed['key'], version=int(completed['version']), path=completed['data']['path'], item=item)



     

if __name__=="__main__":
    main()

