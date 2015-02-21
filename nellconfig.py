from ConfigParser import ConfigParser
from nlpgo import *

class NELLConfig(dict):
    def __init__(self, configParser, eng):
        for section in configParser.sections():
            sectionDict = dict()

            for key,value in configParser.items(section):
                keyParts = key.split('_')
                curDict = sectionDict
                for i in range(0, len(keyParts) - 1):
                    if keyParts[i] not in curDict:
                        curDict[keyParts[i]] = dict()
                    curDict = curDict[keyParts[i]]
                curDict[keyParts[len(keyParts)-1]] = value

            self[section] = sectionDict

            eng.setConfigValue('MitiePosTagger', section + '_Model', sectionDict['nlpgo']['mitiepostaggermodelpath'])
            eng.setConfigValue('MitieNER', section + '_Model', sectionDict['nlpgo']['mitienermodelpath'])        


