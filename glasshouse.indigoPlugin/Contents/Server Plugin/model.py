import sqlite3 as lite
import db

class GlobalSettings(object):
    lite_schema = "CREATE TABLE IF NOT EXISTS GlobalSettings (key STRING UNIQUE, value STRING)"
    indexes = []

    def __init__(self, gh_username):
        self.key = key
        self.value = value

    @classmethod
    def set(self, key, value):
        con = db._get_connection()
        c = con.cursor()
        c.execute('INSERT OR REPLACE INTO GlobalSettings (key, value) values (?, ?)', (key, value))
        # c.execute('UPDATE GlobalSetting SET value=%s WHERE key=%s' % (value, key))
        con.commit()
        setattr(db.GLOBALSETTINGS, key, value)





sqlite_table_models = [GlobalSettings]