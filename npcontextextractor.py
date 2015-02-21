#!/usr/bin/env python

from nlpgo import *
import re
from postagclass import PosTagClass
from nertagclass import NERTagClass
from npcontext import NPContext

class NPContextExtractor(core.Algorithm):
    def __init__(self, name, nellConfig):
        super(self.__class__, self).__init__()
        self._nellConfig = nellConfig

        self._REGEX_TYPE_NP = 'np'
        self._REGEX_TYPE_BEFORE = 'contextbefore'
        self._REGEX_TYPE_AFTER = 'contextafter'
        
        self._POS_TAG_CLASS_PATTERN = re.compile('<p:([^>]*)>')
        self._NER_TAG_CLASS_PATTERN = re.compile('<ner:([^>]*)>')


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
        
        if not self._makeRegexPatterns(doc):
            return False
        
        npContexts = []
        for sen in doc.get('Sentences'):
            npContexts.extend(self._extractFromSentence(doc, sen))
        
        #doc.put(AnnotationList(npContexts))
        
        return True



    def _extractFromSentence(self, doc, sen):
        senStr =  self._makeSentenceString(doc, sen)
        tokens = []
        tokens.extend(doc.get('Tokens'))
        npContexts = []

        for npPattern in self._npPatterns.values():

            matches = npPattern.finditer(senStr)
            for match in matches:
                beforeStr = senStr[:match.start()]
                afterStr = senStr[match.end():]

                matchStartTokenIndex = beforeStr.count(' ')
                matchEndTokenIndex = match.group().count(' ') + matchStartTokenIndex
                
                npLocation = core.Span(tokens[matchStartTokenIndex].location.start, tokens[matchEndTokenIndex - 1].location.end)
                beforeLocations = []
                afterLocations = []

                for beforePattern in self._beforePatterns.values():
                    beforeMatches = beforePattern.finditer(beforeStr)
                    for beforeMatch in beforeMatches:
                        beforeMatchStartTokenIndex = senStr[:beforeMatch.start()].count(' ')
                        beforeMatchEndTokenIndex = matchStartTokenIndex
                        beforeLocations.append(core.Span(tokens[beforeMatchStartTokenIndex].location.start, tokens[beforeMatchEndTokenIndex - 1].location.end))

                for afterPattern in self._afterPatterns.values():
                    afterMatches = afterPattern.finditer(afterStr)
                    for afterMatch in afterMatches:
                        afterMatchStartTokenIndex = matchEndTokenIndex
                        afterMatchEndTokenIndex = matchEndTokenIndex + afterStr[:afterMatch.end()].count(' ')
                        afterLocations.append(core.Span(tokens[afterMatchStartTokenIndex].location.start, tokens[afterMatchEndTokenIndex - 1].location.end))

                npContexts.append(NPContext(npLocation, beforeLocations, afterLocations))

        return npContexts


    def _makeSentenceString(self, doc, sen):
        posTags = doc.get('PosTags').fwdIn(sen)
        ner = doc.get('NamedEntities').fwdIn(sen)
        
        senStr = ''
        for posTag in posTags:
            tagsStr = posTag.tag + ','
            
            for ne in ner:
                if ne.location.contains(posTag.location):
                    tagsStr = tagsStr + ne.tag + ','
            if (len(tagsStr) > 0):
                tagsStr = tagsStr[:-1]

            senStr += tagsStr + ' '

        return senStr


    def _makeRegexPatterns(self, doc):
        regexes = self._nellConfig[str(doc.get('Language'))]['regex']

        self._beforePatterns = dict()
        if self._REGEX_TYPE_BEFORE in regexes:
            for key,value in regexes[self._REGEX_TYPE_BEFORE].items():
                self._beforePatterns[key] = self._makeRegexPattern(value, self._REGEX_TYPE_BEFORE)

        self._afterPatterns = dict()
        if self._REGEX_TYPE_AFTER in regexes:
            for key,value in regexes[self._REGEX_TYPE_AFTER].items():
                self._afterPatterns[key] = self._makeRegexPattern(value, self._REGEX_TYPE_AFTER)

        self._npPatterns = dict()
        if 'np' in regexes:
            for key, value in regexes[self._REGEX_TYPE_NP].items():
                self._npPatterns[key] = self._makeRegexPattern(value, self._REGEX_TYPE_NP)

        return True


    # Note that this assumes that there are no pos tags that are also ner tags
    def _makeRegexPattern(self, regex, regexType):
        transformedRegex = ''

        if regexType == self._REGEX_TYPE_AFTER:
            transformedRegex += '^'
        
        transformedRegex += regex
        
        posTagClassPatternMatch = self._POS_TAG_CLASS_PATTERN.search(transformedRegex)
        while posTagClassPatternMatch:
            posTagsPattern = '('
            posTagClassStrs = posTagClassPatternMatch.group(1).split(',')
            for posTagClassStr in posTagClassStrs:
                posTagClass = PosTagClass.fromString(posTagClassStr)
                for posTag in posTagClass:
                    posTagsPattern += posTag + '|'
            posTagsPattern = posTagsPattern[:-1]
            posTagsPattern += ')'

            patternStart = posTagClassPatternMatch.start()
            patternEnd = posTagClassPatternMatch.end()

            transformedRegex = transformedRegex[:patternStart] + posTagsPattern + transformedRegex[patternEnd:]
            posTagClassPatternMatch = self._POS_TAG_CLASS_PATTERN.search(transformedRegex)

        nerTagClassPatternMatch = self._NER_TAG_CLASS_PATTERN.search(transformedRegex)
        while nerTagClassPatternMatch:
            nerTagsPattern = '('
            nerTagClassStrs = nerTagClassPatternMatch.group(1).split(',')
            for nerTagClassStr in nerTagClassStrs:
                nerTagClass = NERTagClass.fromString(nerTagClassStr)
                for nerTag in nerTagClass:
                    nerTagsPattern += nerTag + '|'
            nerTagsPattern = nerTagsPattern[:-1]
            nerTagsPattern += ')'

            patternStart = nerTagClassPatternMatch.start()
            patternEnd = nerTagClassPatternMatch.end()

            transformedRegex = transformedRegex[:patternStart] + nerTagsPattern + transformedRegex[patternEnd:]
            nerTagClassPatternMatch = self._NER_TAG_CLASS_PATTERN.search(transformedRegex)

        transformedRegex = re.sub('([A-Z$]+)', r'((\S+,\1,\S+\s+)|(\S+,\1\s+)|(\1,\S+\s+)|(\1\s+))', transformedRegex)

        if regexType == self._REGEX_TYPE_BEFORE:
            transformedRegex += '$'

        print regex
        print transformedRegex
        print ''

        return re.compile(transformedRegex)
