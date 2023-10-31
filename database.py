import peewee as pw


database = pw.SqliteDatabase('zotero_cache.db', pragmas={'foreign_keys': 1})

class BaseModel(pw.Model):
    class Meta:
        database = database


class Item(BaseModel):
    zotero_id = pw.CharField(unique=True)
    citation_key = pw.CharField()


class Attachment(BaseModel):
    zotero_id = pw.CharField(unique=True)
    item = pw.ForeignKeyField(Item, on_delete='CASCADE', backref='attachments')
    path = pw.CharField()
    version = pw.IntegerField()

class LibraryVersion(BaseModel):
    version = pw.IntegerField()


def create_tables(*models):
    with database:
        database.create_tables(models)

def create_all_tables():
    create_tables(Item, Attachment, LibraryVersion)