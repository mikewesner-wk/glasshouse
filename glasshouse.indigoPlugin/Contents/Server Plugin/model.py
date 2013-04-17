class GlobalSettings(object):
    lite_schema = "(key STRING, value STRING)"

    def __init__(self, gh_username):
        self.key = key
        self.value = value

    def get(self, key):
        import db
        return db.GLOBALSETTINGS.get(key)

    def set(self, key, value):
        import db
        if db.GLOBALSETTINGS.get(key) is None:
            db.insert_globalsetting(key, value)


sqlite_table_models = [GlobalSettings]