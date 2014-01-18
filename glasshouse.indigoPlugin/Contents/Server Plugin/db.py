import indigo
import sqlite3 as lite


#
#
# This file supports a basic key/value storage
class local(object):
    def __clear__(self):
        for k in self.__dict__.keys()[:]:
            del self.__dict__[k]
    def __repr__(self):
        return repr(self.__dict__)

GLOBALSETTINGS = local()


def get(key):
    if hasattr(GLOBALSETTINGS, key):
        return getattr(GLOBALSETTINGS, key)
    return None

def put(key, value):
    import model
    model.GlobalSettings.set(key, value)

def _get_connection():
    con = lite.connect('dbfile')
    return con

def setup():
    import model
    try:
        global GLOBALSETTINGS
        # Database setup
        con = _get_connection()
        c = con.cursor()

        # this should create and add indexes for all models
        for model_class in model.sqlite_table_models:
            c.execute(model_class.lite_schema)
            for model_index in model_class.indexes:
                c.execute(model_index)

        # this puts all the key/value settings in our global
        c.execute("select * from GlobalSettings")
        results = c.fetchall()

        indigo.server.log("Stored Settings:")
        for row in results:
            k, v = row
            indigo.server.log("\t%s, %s" % (k,v))
            setattr(GLOBALSETTINGS, k, v)

        con.commit()

        c.close()
        con.close()

    except lite.Error, error:
        indigo.server.log(str(error))

