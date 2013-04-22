import indigo
import rest
import db
import requests

class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = True

    def __del__(self):
        indigo.PluginBase.__del__(self)

    def startup(self):
        indigo.insteon.subscribeToIncoming()
        indigo.insteon.subscribeToOutgoing()
        indigo.x10.subscribeToIncoming()
        indigo.x10.subscribeToOutgoing()
        indigo.devices.subscribeToChanges() # -> def deviceUpdated(self, origDev, newDev)
        db.setup()

    def shutdown(self):
        pass

    def runConcurrentThread(self):
        """
        This method is called in a newly created thread after the Start
        method finishes executing.
        """
        # this starts a webserver on port 5000
        # We have it create a new ssl context each
        # time this starts up.  Not going to be to
        # picky about the ssl, just want to prevent
        # snooping.

        # this blocks this thread
        rest.app.run(debug=False, host='0.0.0.0', ssl_context='adhoc')

    def stopConcurrentThread(self):
        """
        This method will get called when the IndigoServer wants your plugin
        to stop any threads that it may have created.
        """
        try:
            requests.post('https://127.0.0.1:5000/shutdown')
        except Exception:
            # requests fails of a retry error
            pass

    def insteonCommandReceived(self, cmd):
        pass#self.debugLog(u"insteonCommandReceived: \n" + str(cmd))

    def insteonCommandSent(self, cmd):
        pass# self.debugLog(u"insteonCommandSent: \n" + str(cmd))

    def variableCreated(self, var):
        pass

    def variableUpdated(self, origVar, newVar):
        pass

    def variableDeleted(self, var):
        pass
