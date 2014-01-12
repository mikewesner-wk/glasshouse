"""
models.py

App Engine datastore models

request comes from house, we find it by api key
request comes in from glass, we find it by ___

* Always get device listing from house
* track notification by device address
*

"""


from google.appengine.ext import ndb


# class ExampleModel(ndb.Model):
#     """Example Model"""
#     example_name = ndb.StringProperty(required=True)
#     example_description = ndb.TextProperty(required=True)
#     added_by = ndb.UserProperty()
#     timestamp = ndb.DateTimeProperty(auto_now_add=True)


class IndigoHouse(ndb.Model):
    """
    Key ID: apikey
    """
    owner = ndb.StringProperty()
    host = ndb.StringProperty()
    apikey = ndb.StringProperty()


class Devices(ndb.Model):
    """
    Key ID:
    """
    dev_id = ndb.StringProperty()


class Variables(ndb.Model):
    pass

class Actions(ndb.Model):
    pass


