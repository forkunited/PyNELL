#!/usr/bin/env python


class PosTagClass():
    JJ = frozenset(["JJ","JJR"])
    VB = frozenset(["VBD","VBZ","VBP","VBN","VBG","VB"])
    NNP = frozenset(["NNP","NNPS"])
    NN = frozenset(["NN","NNS"])
    FN = frozenset(["IN","DT","CC","POS"])
    PRP = frozenset(["PRP"])
    RB = frozenset(["RB"])
    CD = frozenset(["CD"])

    @staticmethod
    def fromString(classStr):
        if classStr == "JJ":
            return PosTagClass.JJ
        elif classStr == "VB":
            return PosTagClass.VB
        elif classStr == "NNP":
            return PosTagClass.NNP
        elif classStr == "NN":
            return PosTagClass.NN
        elif classStr == "FN":
            return PosTagClass.FN
        elif classStr == "PRP":
            return PosTagClass.PRP
        elif classStr == "RB":
            return PosTagClass.RB
        elif classStr == "CD":
            return PosTagClass.CD
        else:
            return None
