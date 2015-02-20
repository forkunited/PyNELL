#!/usr/bin/env python

from nlpgo import *

class NPContext(attr.Attribute):
    def __init__(self, location, beforeLocations, afterLocations):
        # Initialize the super
        super(self.__class__, self).__init__(code)
        self.location = location
        self.beforeLocations = beforeLocations
        self.afterLocations = afterLocations
