# -*- coding: UTF-8 -*-

class AlgoFactory():

    SIMPLE_ALGO = 1
    NOLVA_ALGO = 2
    ALGO_DICT = {SIMPLE_ALGO: "Simple",
                 NOLVA_ALGO: "Nolva"}

    @staticmethod
    def GenAlgo(choice, docLoc, docColor):
        if choice == AlgoFactory.SIMPLE_ALGO:
            return SimpleAlgo(docLoc, docColor)
        elif choice == AlgoFactory.NOLVA_ALGO:
            return NolvaAlgo(docLoc, docColor)
        else:
            return SimpleAlgo(docLoc, docColor)

    @staticmethod
    def GenAlgoInfo():
        return "".join(["%d. %s\n" % (i, AlgoFactory.ALGO_DICT[i]) for i in AlgoFactory.ALGO_DICT.keys()])


class PlayAlgo(object):

    def __init__(self, dotLoc, dotColor):
        self.dotLoc = dotLoc
        self.dotColor = dotColor
    
    def PlayDots(self, color, number):
        if number == 1:
            return self.PlayOneDot(color)
        elif number == 2:
            return self.PlayTwoDot(color)
        elif number == 4:
            return self.PlayFourDot(color)
        else:
            return False
    
    def PlayOneDot(self, color):
        Settings.MoveMouseDelay = 0.1
        for i in range(0, 7):
            if self.dotColor[i] == color:
                click(self.dotLoc[i])
                return 1
            elif self.dotColor[i+7] == color:
                click(self.dotLoc[i + 7])
                return 1
        return 0
    
    def PlayTwoDot(self, color):
        Settings.MoveMouseDelay = 0.5
        for i in range(0, 7): #verical
            if self.dotColor[i] == color and self.dotColor[i + 7] == color :
                dragDrop(self.dotLoc[i], self.dotLoc[i + 7])
                #print "%s, 2" % color
                return 1
        for i in range(0, 6): #horizontal
            if self.dotColor[i] == color and self.dotColor[i + 1] == color:
                dragDrop(self.dotLoc[i], self.dotLoc[i + 1])
                #print "%s, 2" % color
                return 1
            if self.dotColor[i + 7] == color and self.dotColor[i + 8] == color:
                dragDrop(self.dotLoc[i + 7], self.dotLoc[i + 8])
                #print "%s, 2" % color
                return 1
        return 0
    
    def PlayFourDot(self, color):
        Settings.MoveMouseDelay = 0.5
        for i in range(0, 6): #verical
            if self.dotColor[i] == color and\
               self.dotColor[i + 1] == color and\
               self.dotColor[i + 7] == color and\
               self.dotColor[i + 8] == color:
                dragDrop(self.dotLoc[i], self.dotLoc[i + 8])
                #print "%s, 4" % color
                return 1
        return 0

    def Play(self):
        return NotImplemented


class SimpleAlgo(PlayAlgo):

    def Play(self):
        for number in (4, 2, 1):   
            for color in ("b", "w", "y"):
                if self.PlayDots(color, number):
                    return


class NolvaAlgo(SimpleAlgo):

    def Play(self):
        if self.PlayDots("b", 1):
            return
        # super(SimpleAlgo, self).Play()
        for number in (4, 2, 1):   
            for color in ("b", "w", "y"):
                if self.PlayDots(color, number):
                    return
