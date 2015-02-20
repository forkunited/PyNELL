#!/usr/bin/env python

from nlpgo import *

class NPContextExtractor(core.Algorithm):
    def __init__(self, name="NPContextExtractor", nellConfig):
        super(self.__class__, self).__init__()
        self.regexes = nellConfig[str(language)]['regex']



    def provides(self):
        providedAttrs = util.TypeList()
        providedAttrs.add('NPContexts')
        return providedAttrs



    def run(self, doc, eng):
        eng.run(doc, 'Language')
        eng.run(doc, 'PosTags', 'MitiePosTagger')
        eng.run(doc, 'NamedEntities', 'MitieNER')
        eng.run(doc, 'Tokens')
        eng.run(doc, 'Sentences')

        npContexts = []
        for sen in doc.get('Sentences'):
            npContexts.extend(self._extractFromSentence(doc, sen))

        doc.put(npContexts)
        
        return True



    def _extractFromSentence(self, doc, sen):
        #FIXME
        #for sen in doc.get ('Sentences'):
        #    print '%s : %s' % (sen.location, sen.extractContent(doc))
        #    for tok in doc.get('Tokens').fwdIn(sen):
        #        print '    %s : %s' % (tok.location, tok.extractContent(doc))
        
        #doc.get('Language')
        #for ne in doc.get('NamedEntities'):
        #   print '%s : %s %s' % (ne.extractContent(doc), ne.location, ne.tag)
        #for ne in doc.get('PosTags'):        
        pass


    def _transformRegex(self, regex):
        # FIXME
        pass
