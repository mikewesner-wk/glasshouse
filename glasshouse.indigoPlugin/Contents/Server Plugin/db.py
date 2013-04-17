import sqlite3 as lite
import model

GLOBALSETTINGS = {}


def _get_connection():
    con = lite.connect('dbfile')
    return con


def setup():
    try:
        global GLOBALSETTINGS
        # Database setup
        con = _get_connection()
        c = con.cursor()

        for model_class in model.sqlite_table_models:
            sql = 'create table if not exists %s %s' % (model_class.__name__, model_class.lite_schema)
            c.execute(sql)

        c.execute("select * from GlobalSettings")
        GLOBALSETTINGS = c.fetchone()

        con.commit()

        c.close()
        con.close()

    except lite.Error, error:
        indigo.server.log(str(error))



def insert_globalsetting(key, value):
    con = _get_connection()
    c = con.cursor()
    c.execute('Insert into GlobalSetting values (%s, %s)' % (key, value))
    con.commit()
    GLOBALSETTINGS.set(key, value)
