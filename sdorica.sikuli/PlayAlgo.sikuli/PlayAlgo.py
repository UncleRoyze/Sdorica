# -*- coding: UTF-8 -*-
from java.awt import Robot
from sikuli import *
class AlgoFactory():

    SIMPLE_ALGO = 0
    NOLVA_ALGO = 1
    JIN2_ALGO = 2
    NO1_ALGO = 3
    NO2_ALGO = 4
    NO4_ALGO = 5
    FRIDAY3_ALGO = 6
    THURSDAY4_ALGO = 7
    JIN2NAYA_ALGO = 8
    ALGO_DICT = {SIMPLE_ALGO: "Simple",
                 NOLVA_ALGO: "Nolva",
                 JIN2_ALGO : "Jin2",
                 NO1_ALGO: "No 1",
                 NO2_ALGO: "No 2",
                 NO4_ALGO : "No 4",
                 FRIDAY3_ALGO : "Friday 3",
                 THURSDAY4_ALGO: "Thrsday 4",
                 JIN2NAYA_ALGO: "Jin2Naya" }

    @staticmethod
    def GenAlgo(choice, clock):
        if choice == AlgoFactory.SIMPLE_ALGO:
            return SimpleAlgo(clock)
        elif choice == AlgoFactory.NOLVA_ALGO:
            return NolvaAlgo(clock)
        elif choice == AlgoFactory.JIN2_ALGO:
            return Jin2Algo(clock)
        elif choice == AlgoFactory.NO1_ALGO:
            return No1Algo(clock)
        elif choice == AlgoFactory.NO2_ALGO:
            return No2Algo(clock)
        elif choice == AlgoFactory.NO4_ALGO:
            return No4Algo(clock)
        elif choice == AlgoFactory.FRIDAY3_ALGO:
            return Friday3Algo(clock)
        elif choice == AlgoFactory.THURSDAY4_ALGO:
            return Thursday4Algo(clock)
        elif choice == AlgoFactory.JIN2NAYA_ALGO:
            return Jin2NayaAlgo(clock)
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

    def _check_around(self, robot, x, y):
        color = "?"
        x -= 16 #從最外圍開始
        y -= 16
        for i in range(2):
            x += 8 * i
            y += 8 * i
            for j in range(3):
                for k in range(3):
                    c = robot.getPixelColor(x + j*(16-8*i), y + k*(16-8*i)) # get the color object
                    color = self._check_color(c)   
                    if color <> "?":
                        break
        return color
        
    def GetDotBoard(self, clock):
        #logging.debug("GetDotBoard")
        if exists("lost_message.png", 0.001): 
            return -1
        dotLoc = []
        dotColor = []
        dotLoc.append(self.clock.getCenter().offset(221,475))
        stepX = 96
        stepY = 97
        for i in range(1, 7):
            dotLoc.append(Location(dotLoc[i-1].x+stepX, dotLoc[i-1].y))
        for i in range(0, 7):
            dotLoc.append( Location(dotLoc[i].x, dotLoc[i].y+stepY))
        
        r = Robot()
        question_mark_count = 0
        for i in range(0, 14):
            c = r.getPixelColor(dotLoc[i].x, dotLoc[i].y) # get the color object
            color = self._check_color(c)                     # 檢查該點的顏色
            if color == "?":
                color = self._check_around(r, dotLoc[i].x, dotLoc[i].y)
            if color == "?":
                question_mark_count += 1
                if question_mark_count > 3:    #魂盤有太多沒辨識出來, 則跳過這次魂盤
                    return 0

            dotColor.append(color)
            #crgb = ( c.getRed(), c.getGreen(), c.getBlue() ) # decode to RGB values
            #print dotColor[i]
        self.SetBoard(dotLoc, dotColor)        
        return 1

    def _check_color(self, c):
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
        Settings.MoveMouseDelay = 0.001
        for i in range(0, 7):
            if self.dotColor[i] == color:
                click(self.dotLoc[i])
                return 1
            elif self.dotColor[i+7] == color:
                click(self.dotLoc[i + 7])
                return 1
        return 0
    
    def PlayTwoDot(self, color):
        Settings.MoveMouseDelay = 0.01
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
        Settings.MoveMouseDelay = 0.01
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

    def Make_4x_by_z(self, colorX, colorZ):
        for i in range(0, 5):
            if self.dotColor[i] == colorX and self.dotColor[i + 1] == colorX and self.dotColor[i+8] == colorX and self.dotColor[i+9] == colorX:
                if self.dotColor[i+7] == colorZ:   # x x
                    click(self.dotLoc[i+7])        # z x x
                    return 1                       
            if self.dotColor[i+7] == colorX and self.dotColor[i + 8] == colorX and self.dotColor[i+1] == colorX and self.dotColor[i+2] == colorX:
                if self.dotColor[i] == colorZ:     # z x x
                    click(self.dotLoc[i])          # x x
                    return 1
            if self.dotColor[i] == colorX and self.dotColor[i + 2] == colorX and self.dotColor[i+7] == colorX and self.dotColor[i+8] == colorX:
                if self.dotColor[i+1] == colorZ:   # x z x
                    click(self.dotLoc[i+1])        # x x
                    return 1
            if self.dotColor[i] == colorX and self.dotColor[i+1] == colorX and self.dotColor[i+7] == colorX and self.dotColor[i+9] == colorX:
                if self.dotColor[i+8] == colorZ:   # x x
                    click(self.dotLoc[i+8])        # x z x
                    return 1
            if self.dotColor[i] == colorX and self.dotColor[i + 2] == colorX and self.dotColor[i+7] == colorX and self.dotColor[i+9] == colorX:
                if self.dotColor[i+1] == colorZ and self.dotColor[i+8] == colorZ :  # x z x
                    dragDrop(self.dotLoc[i + 1], self.dotLoc[i + 8])                # x z x
                    return 1
            
        for i in range(0, 4):
            if self.dotColor[i] == colorX and self.dotColor[i + 1] == colorX and self.dotColor[i+9] == colorX and self.dotColor[i+10] == colorX:
                if self.dotColor[i+7] == colorZ and self.dotColor[i+8] == colorZ: # x x
                    dragDrop(self.dotLoc[i + 7], self.dotLoc[i + 8])              # z z x x
                    return 1
            if self.dotColor[i+7] == colorX and self.dotColor[i + 8] == colorX and self.dotColor[i+2] == colorX and self.dotColor[i+3] == colorX:
                if self.dotColor[i] == colorZ and self.dotColor[i+1] == colorZ:   # z z x x
                      dragDrop(self.dotLoc[i], self.dotLoc[i + 1])                # x x
                      return 1
            if self.dotColor[i] == colorX and self.dotColor[i + 1] == colorX and self.dotColor[i+7] == colorX and self.dotColor[i+10] == colorX:
                if self.dotColor[i+8] == colorZ and self.dotColor[i+9] == colorZ: # x x
                      dragDrop(self.dotLoc[i+8], self.dotLoc[i+9])                # x z z x
                      return 1
            if self.dotColor[i+7] == colorX and self.dotColor[i + 8] == colorX and self.dotColor[i] == colorX and self.dotColor[i+3] == colorX:
                if self.dotColor[i+1] == colorZ and self.dotColor[i+2] == colorZ: # x z z x
                      dragDrop(self.dotLoc[i+1], self.dotLoc[i+2])                # x x
                      return 1
        return 0
                  
    def Play(self):
        return NotImplemented


class SimpleAlgo(PlayAlgo):
    
    def Play(self, clock, sub_stage, turn):  
        for number in (4, 2, 1):   
            for color in ("b", "w", "g"):
                if self.PlayDots(color, number):
                    return 1
        return 0

class Jin2Algo(PlayAlgo):
    
    strengthen_count = 0
    
    def Play(self, clock, sub_stage, turn):
 
        if turn == 0:
            self.strengthen_count = 0 

        if self.strengthen_count < 2: 
            if self.PlayDots("g", 2):
                self.strengthen_count += 2
                return 1
            else:
                if self.Make2Dot("g"): #做出讓下回合有兩金
                    return 1
                else:
                    self.strengthen_count = 0 
                    
        if self.strengthen_count < 3:
            if self.PlayDots("w", 2):
                self.strengthen_count += 1
                return 1
            if self.PlayDots("w", 1):
                self.strengthen_count += 1
                return 1

        #敵方有人要攻擊了, 讓鱷魚嘲諷坦
        if exists(Pattern("turn1.png").similar(0.80), 0.001) and not exists("dead_crocodile.png",0.001):
            for number in (4, 1):
                if self.PlayDots("g", number):
                    return 1
        for number in (4, 2, 1):   
            for color in ("w", "b", "g"):
                if self.PlayDots(color, number):
                    return 1
        return 0

class NolvaAlgo(SimpleAlgo):

    def Play(self, clock, sub_stage, turn):
        if self.PlayDots("b", 1):
            return 1
        # super(SimpleAlgo, self).Play()
        for number in (4, 2, 1):   
            for color in ("b", "w", "g"):
                if self.PlayDots(color, number):
                    return 1
        return 0

class No1Algo(SimpleAlgo):

    def Play(self, clock, sub_stage, turn):
        for number in (4, 2):   
            for color in ("b", "w", "g"):
                if self.PlayDots(color, number):
                    return 1
        return 0

class No2Algo(SimpleAlgo):

    def Play(self, clock, sub_stage, turn):
        for number in (4, 1):   
            for color in ("b", "w", "g"):
                if self.PlayDots(color, number):
                    return 1
        return 0
    
class No4Algo(SimpleAlgo):

    def Play(self, clock, sub_stage, turn):
        for number in (1, 2):   
            for color in ("b", "w", "g"):
                if self.PlayDots(color, number):
                    return 1
        return 0
    
class Friday3Algo(SimpleAlgo):

    def __init__(self, clock):
        self.clock = clock
        self.is_4_b = False
              
    def Play(self, clock, sub_stage, turn):
        
        #開場1白
        if turn == 0:
            click(clock.getCenter().offset(196,232))
            if self.PlayDots("w", 1):
                return 1
        if turn == 1:
            if self.PlayDots("g", 2):
                return 1
        if turn == 2:
            if self.PlayDots("b", 2):
                return 1
            if self.PlayDots("b", 4):
                return 1
            if self.PlayDots("b", 1):
                return 1
        return -1

class Thursday4Algo(SimpleAlgo):

    def _check_hp_zero(self, clock):
        wait(3)
        drag(clock.getCenter().offset(348,124))

        if exists(Pattern("zero_hp.png").similar(0.80), 5):
            dropAt(clock.getCenter().offset(348,124))
            return 1
        dropAt(clock.getCenter().offset(348,124))
        return 0
        
    def Play(self, clock, sub_stage, turn):
        if turn == 0:
            if not self.PlayDots("g", 2):
                return -1
            else:
                return 1
            
        if turn == 1:
            click(clock.getCenter().offset(60,480)) #點擊自己的參謀
            if not self.PlayDots("w", 2):
                return -1
            else:
                if self._check_hp_zero(clock):
                    return -1
                else:
                    return 1
        if turn == 2:
            if not self.PlayDots("w", 2):
                return -1
            else:
                if self._check_hp_zero(clock):
                    return -1
                else:
                    return 1
       
        if turn == 3:
            if not self.PlayDots("g", 1):
                return -1
            else:
                if self._check_hp_zero(clock):
                    return -1              
                wait(50)
                exit
        return 0

class Jin2NayaAlgo(SimpleAlgo):

    def __init__(self, clock):
        self.clock = clock
        self.is_4_b = False
        self.b1_count = 0
              
    def Play(self, clock, sub_stage, turn):
        if sub_stage < 3:
            if turn > 4:
                return -1
            
        # 紀錄易傷
        if self.b1_count:
            self.b1_count -= 1
        #開場2白
        if turn == 0:
            if self.PlayDots("w", 4):
                return 1
            if self.PlayDots("w", 2):
                return 1
        if turn == 1:
            if self.PlayDots("g", 2):
                return 1
        if turn > 1:
            if self.b1_count == 0:
                if self.PlayDots("b", 1):
                    self.b1_count = 3
                    return 1
            for number in (4, 2):   
                for color in ("b"):
                    if self.PlayDots(color, number):
                        return 1
            if not exists("dead_crocodile.png",0.001):
                for number in (4, 2, 1):
                    if self.PlayDots("g", number):
                        return 1
            for number in (4, 2):   
                for color in ("w"):
                    if self.PlayDots(color, number):
                        return 1
        return -1