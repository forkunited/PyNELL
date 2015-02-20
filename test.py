from ConfigParser import ConfigParser

from nlpgo import *

from nellconfig import NELLConfig
from npcontext import NPContext
from npcontextextractor import NPContextExtractor





configParser = ConfigParser()
configParser.read('nell.ini')
nellConfig = NELLConfig(configParser)


doc = core.Document('Shefaet is annoying me today')
eng = core.Engine()
algo.registerAlgorithms(eng)
eng.put(NPContextExtractor('NPContextExtractorEnglish', nellConfig)
eng.run(doc, 'DummyLanguage')
print doc.get('Language')
print doc.get('DummyLanguage')
