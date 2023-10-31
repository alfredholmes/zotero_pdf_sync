
from database import Attachment

from list_files import get_files
import requests
import keys

endpoint = "https://api.zotero.org"

def main():
    headers = {
            'Zotero-API-Version': str(3),
            'Zotero-API-Key': keys.API_KEY
    } 

    directory = keys.PDF_DIRECTORY
    exclude_directory = keys.SEARCH_EXCLUDE 

    files = get_files(directory) 
    files = [str(file).split(keys.ZOTERO_ROOT)[1] for file in files]

    to_delete = []

    for attachment in Attachment:
        if exclude_directory in attachment.path[:len(exclude_directory)]:
            continue

        relative_path = attachment.path[len('attachments:'):]
        if relative_path not in files:
            to_delete.append(attachment)

    for attachment in to_delete:
        headers['If-Unmodified-Since-Version'] = str(attachment.version)
        r = requests.delete(f'{endpoint}/users/{keys.USER_ID}/items/{attachment.zotero_id}', headers=headers)
        print(r.text)
        attachment.delete_instance()
        
if __name__=="__main__":
    main()

