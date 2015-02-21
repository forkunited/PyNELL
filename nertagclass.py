#!/usr/bin/env python


class NERTagClass():
    ANY = frozenset(["PERSON","LOCATION","ORGANIZATION"])

    @staticmethod
    def fromString(classStr):
        if classStr == "ANY":
            return NERTagClass.ANY
        else:
            return None
    
