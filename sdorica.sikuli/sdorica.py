# -*- coding: UTF-8 -*-
from java.awt import Color
from java.awt import Robot
from time import time
import logging, sys
import AutoLvUp

class PlayModeType:
    ONE_STAGE, AUTO_LV_UP, MATERIAL, QUEST= range(4)

# ----- global setting -----
TURN = 1000
PLAYMODE = PlayModeType.AUTO_LV_UP
TARGETLEVEL_TITLE = Pattern("lv54.png").similar(0.80)
TARGETLEVEL_SMALL = Pattern("TARGETLEVEL_SMALL.png").similar(0.90)
FRIENDS = ["apollo.png", "roy.png", "hcm.png"]
GOOD_BRAINMAN = ["delan_sp.png", "Fatima_lv2.png", "Sione_sp.png", "Shirley_lv3.png", "Shirley_lv2.png", "YanBo_lv3.png"]
# ----- global setting -----
logging.basicConfig(format='%(asctime)s:%(message)s',stream=sys.stdout, level=logging.DEBUG)

class DragCharacterBar:
    topLeft = exists(Pattern("back_button-2.png").targetOffset(460,0),0.001).getCenter()
    dragLeft = topLeft.offset(208, 450)
    dragRight = topLeft.offset(877, 450)

    #角色選單拉到最右邊
    def ToRightEnd(self, dragTimes):       
        for i in range(dragTimes):
            Settings.MoveMouseDelay = 0.1
            Settings.DelayBeforeDrop = 0
            dragDrop(self.dragRight,self.dragLeft)
            wait(1)
    #角色選單拉往左, 一次拉一整排五位位置都正好換掉
    def ToLeft(self):
        Settings.MoveMouseDelay = 0.001
        drag(self.dragLeft)
        Settings.MoveMouseDelay = 1.5
        dropAt(self.dragRight)
        Settings.MoveMouseDelay = 0.001
        hover(self.dragLeft)
    
def SelectBrainman():
    logging.debug("SelectBrainman")
    bar = DragCharacterBar()
    def _findBrainman():
        dragFrom = friendSlotCenter.offset(-510, 240)
        dragTo = friendSlotCenter.offset(-510, 100)
        Settings.MoveMouseDelay = 0.1
        drag(dragFrom)

        selectCenter = None
        trueFriendFound = False
        matches = findAnyList(FRIENDS + GOOD_BRAINMAN)
        if matches:
            for match in matches:
                matchCenter = match.getCenter()
                if match.getIndex() > len(FRIENDS) - 1:
                    selectCenter = matchCenter  # 沒找到朋友的參謀，選其他好用的
                    break
                else:
                    reg = Region(matchCenter.x - 65, matchCenter.y + 20, 140, 200)
                    if reg.exists("using.png"):
                        # 好友的參謀跟自己隊伍的角色相同，只好不選他了 
                        continue
                    selectCenter = reg.getCenter()
                    trueFriendFound = True
                    break
        dropAt(dragTo)
        click(selectCenter)
        return trueFriendFound
        
    friendSlot = exists("SelectFriend.png", 0.001)
    if not friendSlot:
        return
    click(friendSlot)
    friendSlotCenter = friendSlot.getCenter()
    bar.ToRightEnd(1)
    if not _findBrainman():  # drag and drop to second half friends
        bar.ToLeft()
        _findBrainman()


def ClickStartFighting():
    logging.debug("ClickStartFighting")
    Settings.MoveMouseDelay = 0.1
    start = "gotofight.png" 
    if exists(start, 30):
        if not exists(Pattern("SelectFriend.png").similar(0.80), 0.001): # 在選關頁面
            click(start)
            wait(1)
        if PLAYMODE == PlayModeType.AUTO_LV_UP:
            SelectLowLevelCharacter()
        SelectBrainman()
        
        wait(start)
        click(start)
        wait(1)

def DragForward():
    logging.debug("DragForward")
    start_time = time()
    clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
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
    Settings.MoveMouseDelay = 0.1
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
    Settings.MoveMouseDelay = 0.1
    if exists("lost_message.png", 0.001):
        click(Pattern("lost_message.png").targetOffset(0,130))
        logging.debug("lost")
        return 1
    return 0

def GetDotBoard():
    logging.debug("GetDotBoard")
    if exists("lost_message.png", 0.001):
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
    exists(Pattern("clock.png").similar(0.90), 20)              #等到看到有時鐘才代表進入關卡
    
def PlayLevelUp():
    isFailed = False
    ClickStartFighting()
    WaitIntoStage()
    while exists(Pattern("clock.png").similar(0.90) , 0.001):
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
        logging.debug("Turn: %d", i)
        if PLAYMODE == PlayModeType.ONE_STAGE or PLAYMODE == PlayModeType.AUTO_LV_UP:
            PlayLevelUp()
       
    
if __name__ == "__main__":
    #ClickFinish()
    main()
    

#    Pattern("GuildQuest_4.png").similar(0.90)
#    Pattern("1526951100616.png").similar(0.90)
#    Pattern("GuildQuest_no4.png").similar(0.90)
#    "quest_button.png""guildQuest_button.png""material_1.png"Pattern("quest_20turn.png").similar(0.90)Pattern("quest_no4.png").similar(0.90)"back_button.png""material_2.png""material_3.png"
