# -*- coding: UTF-8 -*-
from java.awt import Color
from java.awt import Robot
from time import time
import logging, sys
import AutoLvUp
import ConfigParser

class PlayModeType:
    ONE_STAGE, AUTO_LV_UP, MATERIAL, QUEST= range(4)

# ----- global setting -----
TARGET_LV = 55
FRIENDS = ["apollo.png", "roy.png", "hcm.png"]
GOOD_BRAINMAN = ["delan_sp.png", "Fatima_lv2.png", "Sione_sp.png", "Shirley_lv3.png", "Shirley_lv2.png", "YanBo_lv3.png"]
MATERIALS =  []
for i in range (0, 10):                              
    MATERIALS.append([])              
MATERIALS[1] = [Pattern("stone_2.png").similar(0.80),Pattern("stone_1.png").similar(0.80)]
MATERIALS[5] = [Pattern("fruit_1.png").similar(0.80), Pattern("fruit_2.png").similar(0.80), Pattern("fruit_3.png").similar(0.80), "fruit_4.png", Pattern("1527664800770.png").similar(0.80)]
MATERIALS[7] = [Pattern("masquerade_mask_1.png").similar(0.80), Pattern("masquerade_mask_2.png").similar(0.80), Pattern("masquerade_mask_3.png").similar(0.80), Pattern("masquerade_mask_4.png").similar(0.80)] 
STAGE_TITLE = [Pattern("stage_title_r1.png").similar(0.90),Pattern("stage_title_r2.png").similar(0.90),Pattern("stage_title_r3.png").similar(0.90),Pattern("stage_title_r4.png").similar(0.90),Pattern("stage_title_r5.png").similar(0.90),Pattern("stage_title_r6.png").similar(0.90),Pattern("stage_title_r7.png").similar(0.90)]

# ----- global variables -----

# ----- global variables -----
TURN = 0
PLAYMODE = 0
MATERIAL_STAGE = 0
MATERIAL_SUB_STAGE = 0
# ----- global setting -----
logging.basicConfig(format='%(asctime)s:%(message)s',stream=sys.stdout, level=logging.DEBUG)

class MouseDragHandler:

    def __init__(self, dragFrom, dragTo, reverseOperation=False):
        self.dragFrom = dragFrom
        self.dragTo = dragTo
        self.reverseOperation = reverseOperation

    def __enter__(self):
        if not self.reverseOperation:
            drag(self.dragFrom)
            hover(self.dragTo)
        else:
            dropAt(self.dragTo)

    def __exit__(self, type, value, traceback):
        if not self.reverseOperation:
            dropAt(self.dragTo)
        else:
            drag(self.dragFrom)
            hover(self.dragTo)


class DragCharacterBar:

    def __init__(self):       
        topLeft = exists(Pattern("back_button.png").targetOffset(460,0),0.001).getCenter()
        self.dragLeft = topLeft.offset(208, 450)
        self.dragRight = topLeft.offset(877, 450)
         
    #角色選單拉到最右邊
    def ToRightEnd(self, dragTimes):       
        for i in range(dragTimes):
            Settings.MoveMouseDelay = 0.1
            Settings.DelayBeforeDrop = 0
            dragDrop(self.dragRight, self.dragLeft)
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
        
        selectCenter = None
        trueFriendFound = False         
        with MouseDragHandler(dragFrom, dragTo):
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
    global PLAYMODE
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

def CollectMaterials(clock, dragFrom, dragTo): 
    global PLAYMODE
    global MATERIAL_STAGE
    logging.debug("CollectMaterials")
    if PLAYMODE != PlayModeType.MATERIAL:
        logging.debug("Not in material collecting mode.")
        return
    region = Region(clock.x-130, clock.y-47, 1280, 720)
    matches = region.findAnyList(MATERIALS[MATERIAL_STAGE])
    if not matches:
        logging.debug("Materials not found")
        return

    # Material found! Try to collect it.
    # Go back
    if dragFrom <> None:
        dragBack = Location(dragFrom.x-20, dragFrom.y)
        hover(dragBack)
        wait(0.35)
    with MouseDragHandler(dragFrom, dragTo, True):
        for match in matches:
            index = match.getIndex()
            logging.debug("Found a material with index [%d]" % index)
            material = exists(MATERIALS[MATERIAL_STAGE][index], 0.001)
            if material:
                logging.debug("Trying to collect a material with index [%d]" % index)
                click(material)
            else:
                logging.warning("Material seems disappear, keep moving...")


def DragForward():
    global PLAYMODE
    logging.debug("DragForward")
    start_time = time()
    clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
    if clock:
        dragFrom = clock.getCenter().offset(100,400)
        if PLAYMODE == PlayModeType.MATERIAL:
            # 不能走太快，不然會抓不到素材
            dragTo = Location(dragFrom.x+35, dragFrom.y)
        else:
            dragTo = Location(dragFrom.x+500, dragFrom.y)
        Settings.MoveMouseDelay = 0.5

        with MouseDragHandler(dragFrom, dragTo):
            while not exists("board.png", 0.001):
                CollectMaterials(clock, dragFrom, dragTo)
                end_time = time()
                time_taken = end_time - start_time # time_taken is in seconds
                if(time_taken >= 30): # not found
                    break            #exit while not exists

            logging.debug("in to drag soul mode")

   
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
        for color in ("b", "w", "y"):
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
    
def Play():
    isFailed = False
    ClickStartFighting()
    WaitIntoStage()
    clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
    while clock:
        CollectMaterials(clock, dragFrom=None, dragTo=None)  # 距離起點很近的素材在移動後會來不及找到，所以在移動前先找一次
        DragForward() 
        PlayDrag()
        if CheckLost():            #檢查有無輸
            isFailed = True
            wait(5)
            break
        clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
    if not isFailed:    #正常跳出才要去按Finish
        ClickFinish()

def StartAsking():
    global TURN
    global PLAYMODE
    global MATERIAL_STAGE
    global MATERIAL_SUB_STAGE
    # get the directory containing your running .sikuli
    iniPath = os.path.dirname(getBundlePath())
    if not iniPath in sys.path: sys.path.append(iniPath)
    iniPath = iniPath + "\\sdorica.sikuli\\config.ini"
    #read ini
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(iniPath)
    ini_mode = config.get("setting", "mode")
    PLAYMODE = int(input("Please enter Mode:\n1.One stage\n2.Auto level up\n3.Material\n4.Quest", ini_mode)) - 1
    if PLAYMODE < 0: 
        exit
    ini_turn = config.get("setting", "turn")
    TURN = int(input("How may turns?", ini_turn))
    if TURN < 0:
        exit
    if PLAYMODE == PlayModeType.MATERIAL:
        ini_stage = config.get("material", "stage")
        ini_sub_stage = config.get("material", "sub_stage")
        MATERIAL_STAGE = int(input("Please enter stage:\n1.G Stone\n2.B Bear\n3.W Seed\n4.G Candlestick\n5.W Branches\n6.G Snake\n7.B Doll", ini_stage))
        MATERIAL_SUB_STAGE = int(input("Please enter sub stage:", ini_sub_stage))
        config.set("material", "stage", str(MATERIAL_STAGE))
        config.set("material", "sub_stage", str(MATERIAL_SUB_STAGE))
    #write ini
    config.set("setting", "mode", str(PLAYMODE+1))
    config.set("setting", "turn", str(TURN))
    config.write(open(iniPath, 'wb'))

def EnterStage():
    global PLAYMODE
    global MATERIAL_STAGE
    global MATERIAL_SUB_STAGE
    if PLAYMODE == PlayModeType.MATERIAL:
        region_menu_btn = exists(Pattern("menubtn_region.png").similar(0.80), 0.001)
        if region_menu_btn:
            click(region_menu_btn)
            wait(1)
        region_menu_btn_selected = exists(Pattern("menubtn_region_selected.png").similar(0.80),0.001)
        if region_menu_btn_selected:
            click(region_menu_btn_selected.getCenter().offset(-300,-300))
            wait(1)
        region_title = exists(Pattern("stage_title.png").similar(0.80), 1)
        if region_title:
            while not exists(STAGE_TITLE[MATERIAL_STAGE-1],0.001):
                click(Pattern("next_arrow.png").similar(0.85))
                wait(1)
            for i in range(3):
                Settings.MoveMouseDelay = 0.1
                Settings.DelayBeforeDrop = 0   # back to top
                dragDrop(region_title.getCenter().offset(0,240), region_title.getCenter().offset(0,640))
            wait(1)
            Settings.MoveMouseDelay = 0.1
            Settings.DelayBeforeDrop = 2
            for i in range(MATERIAL_SUB_STAGE-1):
                dragDrop(region_title.getCenter().offset(0,440), region_title.getCenter().offset(0,240))
         
def main():
    global TURN
    StartAsking()
    EnterStage()
    for i in range(TURN):
        logging.debug("Turn: %d", i)
        Play()
       
    
if __name__ == "__main__":
    main()
    

#    Pattern("GuildQuest_4.png").similar(0.90)
#    Pattern("1526951100616.png").similar(0.90)
#    Pattern("GuildQuest_no4.png").similar(0.90)
#    "quest_button.png""guildQuest_button.png""material_1.png"Pattern("quest_20turn.png").similar(0.90)Pattern("quest_no4.png").similar(0.90)"back_button.png""material_2.png""material_3.png"
