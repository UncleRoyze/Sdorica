# -*- coding: UTF-8 -*-
from java.awt import Color
from java.awt import Robot
from time import time
import logging, sys

class PlayModeType:
    LEVELUP, LEVELUP_ALL, MATERIAL, QUEST= range(4)

# ----- global setting -----
TURN = 1000
PLAYMODE = PlayModeType.LEVELUP_ALL
TARGETLEVEL_TITLE = Pattern("lv54.png").similar(0.80)
TARGETLEVEL_SMALL = Pattern("TARGETLEVEL_SMALL.png").similar(0.90)
GOOD_BRAINMAN = ["delan_sp.png", "Sione_sp.png", "Shirley_lv2.png", "Shirley_lv3.png", "Fatima_lv2.png"]
# ----- global setting -----
logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)

def SelectLowLevelCharacter():
    logging.debug("SelectLowLevelCharacter")
    topLeft = exists("back_button.png",0.001).getCenter()
    dragLeft = topLeft.offset(208, 450)
    dragRight = topLeft.offset(877, 450)
    dragLeftLeft = topLeft.offset(100, 450)
    
    def _ToEndOfCharacterBar():
        for i in range(3):
            Settings.MoveMouseDelay = 0.1
            Settings.DelayBeforeDrop = 0
            dragDrop(dragRight,dragLeft)
            wait(1)
        
    def _DragCharacterBar():
        Settings.MoveMouseDelay = 1.5
        dragDrop(dragLeft,dragRight)
        Settings.MoveMouseDelay = 0
        hover(dragLeft)
        
    def _SelectCharacter():
        logging.debug("_SelectCharacter")         
        _ToEndOfCharacterBar()
        for i in range(2):              #會滑動角色選單兩次
            for j in range(4,-1,-1):    #檢查選單中的五個角色
                reg = Region()
                reg.setROI(topLeft.x+115+j*160, topLeft.y+340, 190, 240)
                if reg.exists("using.png", 0.001):
                    continue
                if not reg.exists(TARGETLEVEL_SMALL, 0.001):
                    reg.click(reg.getCenter())
                    return True
                else:
                    return False
            _DragCharacterBar()
        return False

    def _SelectSupport():
        logging.debug("_SelectSupport")
        reg = Region()
        reg.setROI(topLeft.x+630, topLeft.y+260, 325, 75)
        if not reg.exists(Pattern("CharactSelected.png").similar(0.60),0.001): #確認是否已經選到該位
            click(topLeft.offset(800,230))
        _ToEndOfCharacterBar()
        for i in range(7):              #會滑動角色選單七次
            for j in range(4,-1,-1):    #檢查選單中的五個角色
                reg = Region()
                reg.setROI(topLeft.x+115+j*160, topLeft.y+340, 190, 240)
                if not reg.exists(Pattern("black_icon.png").similar(0.65), 0.001):
                    continue
                if not reg.exists(TARGETLEVEL_SMALL, 0.001):
                    if not reg.exists("using.png", 0.001):
                        reg.click(reg.getCenter())
                    return True
                else:
                    return False
            _DragCharacterBar()
        return False
        
    def _CheckWhite():
        logging.debug("_CheckWhite")
        reg = Region()
        reg.setROI(topLeft.x+40, topLeft.y+65, 350, 300)
        if reg.exists(TARGETLEVEL_TITLE, 0.001):
            if not reg.exists(Pattern("CharactSelected.png").similar(0.55),0.001): #確認是否已經選到該位
                click(topLeft.offset(200,215))
            return True
        return False

    def _CheckYellow():
        logging.debug("_CheckYellow")
        reg = Region()
        reg.setROI(topLeft.x+460, topLeft.y+65, 300, 300)
        if reg.exists(TARGETLEVEL_TITLE, 0.001):
            if not reg.exists(Pattern("CharactSelected.png").similar(0.55),0.001): #確認是否已經選到該位
                click(topLeft.offset(610,215))
            return True
        return False
    
    if _CheckWhite():
        _SelectCharacter()
    if _CheckYellow():
        _SelectCharacter()
    _SelectSupport()
    
def SelectBrainman():
    logging.debug("SelectBrainman")
    def _findBrainman():
        dragFrom = friendSlotCenter.offset(-500, 240)
        dragTo = friendSlotCenter.offset(-500, 100)
        Settings.MoveMouseDelay = 0.5
        drag(dragFrom)
        hcm = exists("hcm.png", 0.001)
        apollo = exists("apollo.png", 0.001)
        roy = exists("roy.png", 0.001)

        for friend in (apollo, roy, hcm):
            if friend:
                dropAt(dragTo)
                click(friend.getCenter().offset(0, 100))
                return True

        matches = findAnyList(GOOD_BRAINMAN)
        if matches:
            dropAt(dragTo)
            click(matches[0])
            return False
        else:
            dropAt(dragTo)
            return False
        
        return False
        
    friendSlot = exists("SelectFriend.png", 0.001)
    if not friendSlot:
        return
    click(friendSlot)
    friendSlotCenter = friendSlot.getCenter()
    
    if not _findBrainman():  # drag and drop to second half friends
        dragDrop(friendSlotCenter.offset(-50,240), 
                 friendSlotCenter.offset(-1000,240))
        _findBrainman()


def ClickStartFighting():
    logging.debug("ClickStartFighting")
    Settings.MoveMouseDelay = 0
    start = "gotofight.png"
    if exists(start, 30):
        if not exists("SelectFriend.png", 0.001): # 在選關頁面
            click(start)
            wait(1)
            
        if PLAYMODE == PlayModeType.LEVELUP_ALL:
            SelectLowLevelCharacter()           
        SelectBrainman()
        wait(start)
        click(start)
        wait(1)

def DragForward():
    logging.debug("DragForward")
    start_time = time()
    clock = exists("clock.png" , 0.001)
    if clock:
        dragFrom = clock.getCenter().offset(100,400)           
        Settings.MoveMouseDelay = 0.5
        drag(dragFrom)
        hover(Location(dragFrom.x+500, dragFrom.y))
        while not exists("board.png", 1):
            end_time = time()
            time_taken = end_time - start_time # time_taken is in seconds
            if(time_taken >= 30): # not found
                break            #exit while not exists
        logging.debug("in to drag soul mode")
        dropAt(Location(dragFrom.x+500, dragFrom.y)) 

   
def ClickFinish():
    logging.debug("ClickFinish")
    start_time = time()
    Settings.MoveMouseDelay = 0
    while True:
        finish = exists(Pattern("finish_button.png").similar(0.80),1)
        if finish:
            wait(2)
            click(Pattern("finish_button.png").similar(0.80).targetOffset(26,0))
            break
        end_time = time()
        time_taken = end_time - start_time # time_taken is in seconds
        if(time_taken >= 30): # not found
            break

def PlayDots(color, number, dotLoc, dotColor):
    if number == 1:
        return PlayOneDot(color, dotLoc, dotColor)
    elif number == 2:
        return PlayTwoDot(color, dotLoc, dotColor)
    elif number == 4:
        return PlayFourDot(color, dotLoc, dotColor)
    else:
        return False

def PlayOneDot(color, dotLoc, dotColor):
    Settings.MoveMouseDelay = 0.1
    for i in range(0, 7):
        if dotColor[i] == color:
            click(dotLoc[i])
            return 1
        elif dotColor[i+7] == color:
            click(dotLoc[i+7])
            return 1
    return 0

def PlayTwoDot(color, dotLoc, dotColor):
    Settings.MoveMouseDelay = 0.5
    for i in range(0, 7): #verical
        if dotColor[i] == color and dotColor[i+7] == color :
            dragDrop(dotLoc[i], dotLoc[i+7])
            #print "%s, 2" % color
            return 1
    for i in range(0, 6): #horizontal
        if dotColor[i] == color and dotColor[i+1] == color:
            dragDrop(dotLoc[i], dotLoc[i+1])
            #print "%s, 2" % color
            return 1
        if dotColor[i+7] == color and dotColor[i+8] == color:
            dragDrop(dotLoc[i], dotLoc[i+1])
            #print "%s, 2" % color
            return 1
    return 0

def PlayFourDot(color, dotLoc, dotColor):
    Settings.MoveMouseDelay = 0.5
    for i in range(0, 6): #verical
        if dotColor[i] == color and dotColor[i+1] == color and dotColor[i+7] == color and dotColor[i+8] == color:
            dragDrop(dotLoc[i], dotLoc[i+8])
            #print "%s, 4" % color
            return 1
    return 0


def SimpleAlgo(dotLoc, dotColor):
    for number in (4, 2, 1):   
        for color in ("b", "y", "w"):
            if PlayDots(color, number, dotLoc, dotColor):
                return

def C10_2_Algo(dotLoc, dotColor):
    logging.debug("C10_2_Algo")
    if PlayDots("b", 1, dotLoc, dotColor):
        return
    SimpleAlgo(dotLoc, dotColor)

def CheckLost():
    logging.debug("CheckLost")
    Settings.MoveMouseDelay = 0
    if exists(Pattern("ok_button.png").similar(0.90), 0.001):
        click(Pattern("ok_button.png").similar(0.90))
        logging.debug("lost")
        return 1
    return 0

def GetDotBoard():
    logging.debug("GetDotBoard")
    if exists(Pattern("ok_button.png").similar(0.90), 0.001):
        return 0, 0, 0
    if not exists(Pattern("soul_normal.png").similar(0.85), 1):
        if not exists(Pattern("soul_dead.png").similar(0.85), 1):
            return 0, 0, 0
    clock = exists("clock.png", 0.001)
    dotLoc = []
    dotLoc.append(clock.getCenter().offset(221,471))
    stepX = 96
    stepY = 99
    for i in range(1, 7):
        dotLoc.append(Location(dotLoc[i-1].x+stepX, dotLoc[i-1].y))
    for i in range(0, 7):
        dotLoc.append( Location(dotLoc[i].x, dotLoc[i].y+stepY))
    dotColor = []
    r = Robot()
    for i in range(0, 14):
        c = r.getPixelColor(dotLoc[i].x, dotLoc[i].y) # get the color object
        if c.getRed() < 150 and c.getGreen() < 150 and c.getBlue() > 200:
            dotColor.append("b")
        elif c.getRed() > 200 and c.getGreen() > 200 and c.getBlue() < 150:
            dotColor.append("y")
        elif c.getRed() > 220 and c.getGreen() > 220 and c.getBlue() > 220:
            dotColor.append("w")
        else:
            dotColor.append("?")
        #crgb = ( c.getRed(), c.getGreen(), c.getBlue() ) # decode to RGB values
        #print dotColor[i]
    return 1, dotLoc, dotColor
        
def PlayDrag():
    logging.debug("PlayDrag")
    if not exists("clock.png" , 0.001):
        return
    while True:
        isFound, dotLoc, dotColor = GetDotBoard()
        if not isFound:
            break
        C10_2_Algo(dotLoc, dotColor)
        #SimpleAlgo(dotLoc, dotColor)
        wait(1)

def WaitIntoStage():
    wait("clock.png", 20)                #等到看到有時鐘才代表進入關卡
    
def PlayLevelUp():
    isFailed = False
    ClickStartFighting()
    WaitIntoStage()
    while exists("clock.png" , 0.001):
        DragForward() 
        PlayDrag()
        if CheckLost():            #檢查有無輸
            isFailed = True
            wait(5)
            break
    if not isFailed:    #正常跳出才要去按Finish
        ClickFinish()

def main():
    for i in range(TURN):
        print "Turn: ", i
        if PLAYMODE == PlayModeType.LEVELUP or PLAYMODE == PlayModeType.LEVELUP_ALL:
            PlayLevelUp()
       
    
if __name__ == "__main__":
    main()
    

#    Pattern("GuildQuest_4.png").similar(0.90)
#    Pattern("1526951100616.png").similar(0.90)
#    Pattern("GuildQuest_no4.png").similar(0.90)
#    "quest_button.png""guildQuest_button.png""material_1.png"Pattern("quest_20turn.png").similar(0.90)Pattern("quest_no4.png").similar(0.90)"back_button.png"
