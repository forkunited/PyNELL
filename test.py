import sys
from ConfigParser import ConfigParser

from nlpgo import *

from nellconfig import NELLConfig
from npcontext import NPContext
from npcontextextractor import NPContextExtractor

configParser = ConfigParser()
eng = core.Engine()
algo.registerAlgorithms(eng)

configParser.read(sys.argv[1])
nellConfig = NELLConfig(configParser, eng)

eng.put(NPContextExtractor('NPContextExtractor', nellConfig))

doc = core.Document('Joe bakes a cake on his radiator.')
eng.run(doc, 'NPContexts')
doc.get('NPContexts')
