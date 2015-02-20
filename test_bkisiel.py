#!/usr/bin/env python

import sys
from nlpgo import *

eng = core.Engine()
algo.registerAlgorithms(eng)

#modelFile= '/home/bkisiel/rtw/nlpgo0/nlpgo/models/nlpgo_pos_spanish_mitie_conll2003.dat'
modelFile= '/home/bkisiel/rtw/nlpgo0/nlpgo/models/nlpgo_pos_english_mitie_conll2003.dat'
eng.setConfigValue('MitiePosTagger', 'es_Model', modelFile)

modelFile='models/nlpgo_ner_spanish_mitie_conll2002.dat'
eng.setConfigValue('MitieNER', 'es_Model', modelFile)

es_language = attr.Language('es')

# Process one document worth of sentences.  Looking forward, each document can
# be one sentence, as is historically the case with the all-pairs data, where
# we use Hadoop to produce a set of unique sentences over the entire corpus as
# a way to mitigate the effects of text that is repeated exactly.
#
# For now, this writes its real output to stdout, and so has no useful return
# value.  This is primarily because I couldn't figure out how to get Python to
# not seg fault by trying to build a string to print or return (looks like it
# could be some strange interaction with the peculiarities of how the NLPGo
# libraries are implemented).  Routing everything directly to sys.stdout
# circumvents whatever the problem is.  We can come back to this later.
def process_one_document(doc):
    eng.run(doc, 'PosTags', 'MitiePosTagger')
    eng.run(doc, 'NamedEntities', 'MitieNER')
    eng.run(doc, 'Tokens')
    eng.run(doc, 'Sentences')
    
    # Get POS tags for this document in a list that we can advance through as
    # we iterate through the tokens in each sentence.
    poslist = []
    posit = 0
    for postag in doc.get('PosTags'):
        poslist.append(postag)
        
    # Same for NE tags
    nerlist = []
    nerit = 0
    for nertag in doc.get('NamedEntities'):
        nerlist.append(nertag)
            
    # Now iterate through each sentence in the document, and simultaneously
    # iterate through poslist, emitting any overlapping tags for each token in
    # each sentence.
    #
    # This is where Python segfaults if I try to build up each sentence in a
    # string, even before an attempt to print it out.
    for sen in doc.get ('Sentences'):                                                  
        first = 1
        for tok in doc.get('Tokens').fwdIn(sen):
            # Emit token
            if first:
                first = 0
            else:
                sys.stdout.write(' ')
            sys.stdout.write(tok.extractContent(doc))

            # Emit POS tag(s) if any
            while posit < len(poslist) and poslist[posit].location.precedes(tok.location) and not poslist[posit].location.contains(tok.location):
                posit += 1
            offset = 0
            while posit+offset < len(poslist) and poslist[posit+offset].location.contains(tok.location):
                sys.stdout.write('/' + poslist[posit+offset].tag)
                offset += 1

            # Emit NER tag(s) if any
            while nerit < len(nerlist) and nerlist[nerit].location.precedes(tok.location) and not nerlist[nerit].location.contains(tok.location):
                nerit += 1
            offset = 0 
            while nerit+offset < len(nerlist) and nerlist[nerit+offset].location.contains(tok.location):
                sys.stdout.write('/' + nerlist[nerit+offset].tag)
                offset += 1
            
        sys.stdout.write("\n")
    sys.stdout.flush()



with open('/dev/stdin') as f:
    for line in f:
        text = line[line.find("\t")+1:].rstrip()

        # The sentence identifier seems to like to have sentences end with
        # periods, so pop one on the end if necessary.  HTML-derived text
        # often lacks such things.
        if text[len(text)-1] != '.':
            text = text + '.'

        doc = core.Document(text)
        doc.put(es_language, 'test.py')
        process_one_document(doc)

