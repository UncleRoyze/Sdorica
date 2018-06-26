# -*- coding: UTF-8 -*-

class AlgoFactory():

    SIMPLE_ALGO = 0
    NOLVA_ALGO = 1
    JIN2_ALGO = 2
    FRIDAY3_ALGO = 3
    ALGO_DICT = {SIMPLE_ALGO: "Simple",
                 NOLVA_ALGO: "Nolva",
                 JIN2_ALGO : "Jin2",
                 FRIDAY3_ALGO : "Friday 3"}

    @staticmethod
    def GenAlgo(choice, clock):
        if choice == AlgoFactory.SIMPLE_ALGO:
            return SimpleAlgo(clock)
        elif choice == AlgoFactory.NOLVA_ALGO:
            return NolvaAlgo(clock)
        elif choice == AlgoFactory.JIN2_ALGO:
            return Jin2Algo(clock)
        elif choice == AlgoFactory.FRIDAY3_ALGO:
            return Friday3Algo(clock)
        else:
            return SimpleAlgo(clock)

    @staticmethod
    def GenAlgoInfo():
        dictlist = []
        for key, name in AlgoFactory.ALGO_DICT.iteritems():
            dictlist.append(name)
        return dictlist

    @staticmethod
    def GetAlgoIndex(search_name):
        for key, name in AlgoFactory.ALGO_DICT.iteritems():   
            if name == search_name:
                return key
        return -1


class PlayAlgo(object):

    def __init__(self, clock):
        self.clock = clock

    def SetBoard(self, dotLoc, dotColor):
        self.dotLoc = dotLoc
        self.dotColor = dotColor
        
    def GetDotBoard(self):
        logging.debug("GetDotBoard")
        if exists("lost_message.png", 0.001): 
            return -1
        if not exists(Pattern("soul_normal.png").similar(0.85), 1):
            if not exists(Pattern("soul_dead.png").similar(0.85), 1):
                return -1

        dotLoc = []
        dotColor = []
        dotLoc.append(self.clock.getCenter().offset(222,477))
        stepX = 95
        stepY = 97
        for i in range(1, 7):
            dotLoc.append(Location(dotLoc[i-1].x+stepX, dotLoc[i-1].y))
        for i in range(0, 7):
            dotLoc.append( Location(dotLoc[i].x, dotLoc[i].y+stepY))
        
        r = Robot()
        for i in range(0, 14):
            c = r.getPixelColor(dotLoc[i].x, dotLoc[i].y) # get the color object
            for j in range(1,4):
                color = self.CheckColor(c)                     # 檢查該點的顏色
                if color <> "?":
                    break
                c = r.getPixelColor(dotLoc[i].x, dotLoc[i].y-j*3) # 換位置再找一次
            if color == "?":
                return 0
                break
            dotColor.append(color)
            #crgb = ( c.getRed(), c.getGreen(), c.getBlue() ) # decode to RGB values
            #print dotColor[i]
        self.SetBoard(dotLoc, dotColor)
        return 1

    def CheckColor(self, c):
        if c.getRed() < 150 and c.getGreen() < 150 and c.getBlue() > 200:
            return "b"
        elif c.getRed() > 200 and c.getGreen() > 200 and c.getBlue() < 150:
            return "g"
        elif c.getRed() > 220 and c.getGreen() > 220 and c.getBlue() > 220:
            return "w"
        else:
            return "?"
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

    def Make2Dot(self, color):
         for i in range(0, 5): #horizontal
            if self.dotColor[i] == color and self.dotColor[i + 2] == color:
                click(self.dotLoc[i+1])
                return 1
            if self.dotColor[i + 7] == color and self.dotColor[i + 9] == color:
                click(self.dotLoc[i+8])
                return 1
         for i in range(0, 6): #verical
              if self.dotColor[i] == color and self.dotColor[i + 8] == color:
                  click(self.dotLoc[i+7])
                  return 1
              if self.dotColor[i+1] == color and self.dotColor[i + 7] == color:
                  click(self.dotLoc[i])
                  return 1
               
    def Play(self):
        return NotImplemented


class SimpleAlgo(PlayAlgo):
    
    def Play(self, num):  
        for number in (4, 2, 1):   
            for color in ("b", "w", "g"):
                if self.PlayDots(color, number):
                    return

class Jin2Algo(PlayAlgo):
    
    strengthen_count = 0
    
    def Play(self, num):
        if self.PlayDots("b", 4):
            return
        
        if num == 0:
            self.strengthen_count = 0 

        if self.strengthen_count == 0: 
            #if self.PlayDots("w", 4):
            #    self.strengthen_count += 3
            #    return
            if self.PlayDots("w", 1):
                self.strengthen_count += 1
                return

        if self.strengthen_count < 3:
            if self.PlayDots("g", 2):
                self.strengthen_count += 2
                return
            else:
                if self.Make2Dot("g"): #做出讓下回合有兩金
                    return
                else:
                    self.strengthen_count = 0

        #敵方有人要攻擊了, 讓鱷魚嘲諷坦
        if exists(Pattern("turn1.png").similar(0.80), 0.001):
            for number in (4, 1):
                if self.PlayDots("g", number):
                    return
        for number in (4, 2, 1):   
            for color in ("w", "b", "g"):
                if self.PlayDots(color, number):
                    return

class NolvaAlgo(SimpleAlgo):

    def Play(self, num):
        if self.PlayDots("b", 1):
            return
        # super(SimpleAlgo, self).Play()
        for number in (4, 2, 1):   
            for color in ("b", "w", "g"):
                if self.PlayDots(color, number):
                    return

class Friday3Algo(SimpleAlgo):

    def Play1(self):
        if self.PlayDots("w", 1):
            return
    def Play2(self):
        if self.PlayDots("w", 1):
            return
    def Play3(self):
        if self.PlayDots("b", 4):
            return
        if self.PlayDots("b", 2):
            return
