# Zotero PDF Sync
Sync pdf attachments to zotero

This is a collection of python scripts that scans the files in a folder and checks whether there are any pdf files that widh filenames that begin with a citation key of an zotero bibliography item. If there are then the scripts add the files as an attachment to corresponding zotero item. At the moment the scripts assume that they are scanning files that are contained in the Zotero base directory and the files are attached as linked files, that is, the files are not uploaded to the zotero cloud storage.

## How to use
WARNING: These scripts could potentially delete attachments from your zotero libary if not properly configured.

### Installation
To run clone the repository and install `peewee` and `requests` using
```
$ pip isntall peewee requests
```

Then create a file `keys.py` with the following contents

```python
API_KEY = "Zotero API KEY with Write Access"
USER_ID = "Your Zotero user Id"

PDF_DIRECTORY = 'absoulte path of the directory you want to search'
ZOTERO_ROOT = 'Your zotero base directory with trailing forward slash, eg: /home/user/zotero_base/'
SEARCH_EXCLUDE = 'attachments:References' #this is a parameter that ignores any references that you don't want to mess with. For example, if you store all your actual pdfs in zotero_base/Refernces and you don't want these scripts to interfere with these.
```

The reccomended setup for this is to have a Zotero base directory where you have a folder structure as follows

```
base_directory:
  References:
    Zotero managed pdf references
  NotePDFs:
    Folder of pdfs that begin with citation keys
```

Settings for this setup would be, if the base directory is /home/user/base_directory

```
PDF_DIRECTORY = '/home/user/zotero_base/NotePDFs'
ZOTERO_ROOT = '/home/user/base_directory/'
SEARCH_EXCLUDE = 'attachments:References'
```

and the scripts will check whether there are pdfs in NotePDFs that start with a citation key and if so then add a linked file to the zotero item.

### Zotero configuration

To use this with zotero, each item needs to have it's citation key in the `extra` tag such that the extra field contains text of the form
```
some info...
Citation Key: theCitationKey
some other info...
```

This can be achived automatically using better bibtex and setting it to automatically pin the citation keys in the better bibtex settings.
