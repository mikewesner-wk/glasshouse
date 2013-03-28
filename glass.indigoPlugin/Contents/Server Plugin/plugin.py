#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2012, Perceptive Automation, LLC. All rights reserved.
# http://www.perceptiveautomation.com

import os
import sys
import rest

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = True
        # this starts a webserver on port 5000
        rest.app.run()

    def __del__(self):
        indigo.PluginBase.__del__(self)

    ########################################
    def startup(self):
        self.debugLog(u"startup called -- subscribing to all X10 and INSTEON commands")
        indigo.insteon.subscribeToIncoming()
        indigo.insteon.subscribeToOutgoing()
        indigo.x10.subscribeToIncoming()
        indigo.x10.subscribeToOutgoing()

    def shutdown(self):
        self.debugLog(u"shutdown called")

    ########################################
    def insteonCommandReceived(self, cmd):
        self.debugLog(u"insteonCommandReceived: \n" + str(cmd))

    def insteonCommandSent(self, cmd):
        self.debugLog(u"insteonCommandSent: \n" + str(cmd))


