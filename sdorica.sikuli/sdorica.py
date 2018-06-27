# -*- coding: UTF-8 -*-
from java.awt import Color
from java.awt import Robot
import datetime
from time import time
import logging, sys
import AutoLvUp
reload(AutoLvUp)
import config
reload(config)
import PlayAlgo
reload(PlayAlgo)

configObj = config.Configuration()
logging.basicConfig(format='%(asctime)s:%(message)s',stream=sys.stdout, level=logging.INFO)


class PlayModeType:
    ONE_STAGE, AUTO_LV_UP, MATERIAL, QUEST = range(4)


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
            matches = findAnyList(configObj.friends + configObj.brainmen)
            if matches:
                for match in matches:
                    matchCenter = match.getCenter()
                    if match.getIndex() > len(configObj.friends) - 1:
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
    logging.debug("ClickStartFighting")
    if exists(Pattern("clock.png").similar(0.90) , 0.001):
        return
    Settings.MoveMouseDelay = 0.1
    start = "gotofight.png" 
    if exists(start, 30):
        wait(3)
        if not exists(Pattern("SelectFriend.png").similar(0.90), 0.001): # 在選關頁面
            click(start)
            wait(1)
        if configObj.getPlayMode() == PlayModeType.AUTO_LV_UP:
            SelectLowLevelCharacter(configObj.target_lv)
        SelectBrainman()
        wait(start)
        click(start)
        wait(1)


def CollectMaterials(clock, dragFrom, dragTo):
    logging.debug("CollectMaterials")
    if configObj.getPlayMode() != PlayModeType.MATERIAL:
        logging.debug("Not in material collecting mode.")
        return

    region = Region(clock.x-130, clock.y-47, 1280, 720)
    material_stage = configObj.getMaterialStage()
    matches = region.findAnyList(configObj.materials[material_stage])
    if not matches:
        logging.debug("Materials not found")
        return

    # Material found! Try to collect it.
    # Go back
    logging.debug("Material found!")
    if dragFrom is not None:
        dragBack = Location(dragFrom.x-20, dragFrom.y)
        hover(dragBack)
        wait(0.35)

    with MouseDragHandler(dragFrom, dragTo, True):
        for match in matches:
            index = match.getIndex()
            logging.debug("Found a material with index [%d]" % index)
            material = exists(configObj.materials[material_stage][index], 0.001)
            if material:
                logging.debug("Trying to collect a material with index [%d]" % index)
                click(material)
            else:
                logging.warning("Material seems disappear, keep moving...")


def DragForward():
    logging.debug("DragForward")
    start_time = time()
    clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
    if clock:
        dragFrom = clock.getCenter().offset(100,400)
        if configObj.getPlayMode() == PlayModeType.MATERIAL:
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
    isReward = True
    while True:
        finish = exists(Pattern("finish_button.png").similar(0.80),1)
        if finish:        # 因為一開始檢測到的按鈕位置會變動
            if configObj.getPlayMode() == PlayModeType.ONE_STAGE:
                if exists(Pattern("zero_money.png").exact(), 2):    #沒有庫倫了, 則跳出
                    isReward = False
            wait(2)
            click(Pattern("finish_button.png").similar(0.80).targetOffset(26,0))
            break
        network_lost = exists("network_lost.png",0.001)
        if network_lost:
            click(network_lost.offset(0,140))
        end_time = time()
        time_taken = end_time - start_time # time_taken is in seconds
        if(time_taken >= 60): # not found
            break
    return isReward

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
    dotLoc.append(clock.getCenter().offset(221,475))
    stepX = 96
    stepY = 97
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
    clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
    if not clock:
        return
    while True:
        isFound, dotLoc, dotColor = GetDotBoard()
        if not isFound:
            break
        click(clock.getCenter().offset(60,480))
        playAlgo = AlgoFactory.GenAlgo(configObj.getAlgo(), dotLoc, dotColor)
        playAlgo.Play()
        #C10_2_Algo(dotLoc, dotColor)
        #SimpleAlgo(dotLoc, dotColor)
        wait(1)


def WaitIntoStage():
    start_time = time()
    while not exists(Pattern("clock.png").similar(0.90), 0.001):              #等到看到有時鐘才代表進入關卡
        if exists("ok_btn_1.png", 0.001):
                click("ok_btn_1.png")
        if(start_time - time()  >= 30): # not found
            break            #exit while not exists
    

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
        ok = exists("ok_btn_1.png", 0.001)
        if ok:
            click(ok)
        clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
    return isFailed


def StartAsking():
    ini_mode = configObj.config.get("setting", "mode")
    playmode = int(input("Please enter Mode:\n1.One stage\n2.Auto level up\n3.Material\n4.Quest", ini_mode)) - 1
    if playmode < 0:
        exit
    configObj.config.set("setting", "mode", str(playmode + 1))
    
    ini_turn = configObj.config.get("setting", "turn")
    turn = int(input("How may turns?", ini_turn))
    if turn < 0:
        exit
    configObj.config.set("setting", "turn", str(turn))
    
    if playmode == PlayModeType.MATERIAL:
        ini_stage = configObj.config.get("material", "stage")
        ini_sub_stage = configObj.config.get("material", "sub_stage")
        material_stage = int(input("Please enter stage:\n1.G Stone\n2.B Bear\n3.W Seed\n4.G Candlestick\n5.W Branches\n6.G Snake\n7.B Doll", ini_stage))
        material_sub_stage = int(input("Please enter sub stage:", ini_sub_stage))
        configObj.config.set("material", "stage", str(material_stage))
        configObj.config.set("material", "sub_stage", str(material_sub_stage))
    elif playmode in (PlayModeType.AUTO_LV_UP, PlayModeType.ONE_STAGE):
        ini_challenge_stage = configObj.config.get("challenge", "stage")
        ini_challenge_sub_stage = configObj.config.get("challenge", "sub_stage")
        challenge_stage = int(input("Please enter challenge stage: (1~13)", ini_challenge_stage))
        challenge_sub_stage = int(input("Please enter challenge sub stage: (1~5)", ini_challenge_sub_stage))
        configObj.config.set("challenge", "stage", str(challenge_stage))
        configObj.config.set("challenge", "sub_stage", str(challenge_sub_stage))
        if playmode == PlayModeType.AUTO_LV_UP:
            ini_target_lv = configObj.config.get("setting", "target_lv")
            target_lv = int(input("Please enter your targeted level:", ini_target_lv))
            configObj.config.set("setting", "target_lv", str(target_lv))

    ini_algo = configObj.config.get("setting", "algo")
    algorithm = int(input("Please select algorithm:\n%s" % AlgoFactory.GenAlgoInfo(), ini_algo))
    configObj.config.set("setting", "algo", str(algorithm))

    ini_designated_hour = configObj.config.get("setting", "designated_hour")
    designated_hour = int(input("Please enter your designated time in hour (0~23)\n(-1 mean to run this script right away)", ini_designated_hour))
    if designated_hour not in range(0, 24):
        designated_hour = -1
    configObj.config.set("setting", "designated_hour", str(designated_hour))

    #write ini
    configObj.writeConfig()


def WaitForDesignatedTime():
    logging.debug("Enter WaitForDesignatedTime")
    designated_hour = configObj.getDesignatedHour()
    print "designated hour is %d" % designated_hour
    if designated_hour < 0:
        logging.debug("Run the script right away!")
        return  # run the script right away

    designated_time = datetime.datetime.combine(datetime.date.today(), datetime.time(designated_hour, 0))
    timedelta = designated_time - datetime.datetime.today()
    print "timedelta 1 %s" % timedelta
    if timedelta.days < 0:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        timedelta = datetime.datetime.combine(tomorrow, datetime.time(designated_hour, 0)) - datetime.datetime.today()
    print "timedelta 2 %s" % timedelta
    print "The script is gonna excute in %d seconds." % timedelta.seconds
    wait(timedelta.seconds)


def EnterSdorica():
    app = exists("Sdorica.png", 1)
    if app:
        click(app)
        wait(20)
    else:
        logging.debug("Cannot find Sdorica app")
        return
    app_title = exists("AppTitle.png", 1)
    if app_title:
        click(app_title)
        wait(20)
    else:
        logging.debug("Cannot find Sdorica title")
        return
        
    ad_cancel = exists(Pattern("AdCancel.png").similar(0.90), 1)
    if ad_cancel:
        click(ad_cancel)
        wait(1)
    else:
        logging.debug("Cannot find advertisement cancel button")


def SelectChallengeStage():
    def GetChallengePageAndCount(stage, sub_stage):
        page, count = 0, 0
        if stage in range(1, 6):
            page = 1
            if sub_stage in range(1, 5):
                count = (stage - 1) * 4 + sub_stage - 1
        elif stage in range(6, 14):
            page = ((stage - 6) / 4) + 2
            count = ((stage - 6) % 4) * 5 + sub_stage - 1
        elif stage == 14:
            page = 4
            count = sub_stage - 1
        return page, count

    if configObj.getPlayMode() not in (PlayModeType.ONE_STAGE, PlayModeType.AUTO_LV_UP):
        return
    challenge_btn = exists("ChallengeBtn.png", 0.001) 
    if challenge_btn:
        click(challenge_btn)
        wait(1)
    else:
        logging.debug("Cannot find challenge button, try to find the selected one.")
        
    challenge_btn_selected = exists("ChallengeBtnSelected.png", 0.001)
    if challenge_btn_selected:
        click(challenge_btn_selected)
        wait(1)
    else:
        
        logging.debug("Cannot find seletected challenge button.")
        
    challenge_title = exists(Pattern("challenge_title.png").similar(0.80), 1)
    if not challenge_title:
        return
    challenge_page, challenge_count = GetChallengePageAndCount(configObj.getChallengeStage(), configObj.getChallengeSubStage())
    while not exists(configObj.challenge_stage_title[challenge_page], 0.001):
        click(Pattern("next_arrow.png").similar(0.85))
        wait(1)
    for i in range(7):
        Settings.MoveMouseDelay = 0.1
        Settings.DelayBeforeDrop = 0   # back to top
        dragDrop(challenge_title.getCenter().offset(0, 240), challenge_title.getCenter().offset(0, 640))
    wait(1)
    Settings.MoveMouseDelay = 0.1
    Settings.DelayBeforeDrop = 2
    for i in range(challenge_count):
        dragDrop(challenge_title.getCenter().offset(0, 440), challenge_title.getCenter().offset(0, 240))
    
    
def SelectMaterialStage():
    if configObj.getPlayMode() != PlayModeType.MATERIAL:
        return    
    region_menu_btn = exists(Pattern("menubtn_region.png").similar(0.80), 0.001)
    if region_menu_btn:
        click(region_menu_btn)
        wait(1)
    region_menu_btn_selected = exists(Pattern("menubtn_region_selected.png").similar(0.80), 0.001)
    if region_menu_btn_selected:
        click(region_menu_btn_selected.getCenter().offset(-300, -300))
        wait(1)
    region_title = exists(Pattern("stage_title.png").similar(0.80), 1)
    if region_title:
        while not exists(configObj.material_stage_title[configObj.getMaterialStage() - 1], 0.001):
            click(Pattern("next_arrow.png").similar(0.85))
            wait(1)
        for i in range(3):
            Settings.MoveMouseDelay = 0.1
            Settings.DelayBeforeDrop = 0   # back to top
            dragDrop(region_title.getCenter().offset(0, 240), region_title.getCenter().offset(0, 640))
        wait(1)
        Settings.MoveMouseDelay = 0.1
        Settings.DelayBeforeDrop = 2
        for i in range(configObj.getMaterialSubStage() - 1):
            dragDrop(region_title.getCenter().offset(0, 440), region_title.getCenter().offset(0, 240))

def ChangeStage(i):
   if i % 10 == 0 and i != 0:
        logging.debug("ChangeStage")
        region_title = wait("stage_title_1.png", 10)
        if region_title:
            dragDrop(region_title.getCenter().offset(0, 240), region_title.getCenter().offset(0, 440))

def main():
    StartAsking()
    WaitForDesignatedTime()
    EnterSdorica()
    SelectChallengeStage()
    SelectMaterialStage()
    zero_reward_count = 0
    for i in range(configObj.getTurns()):
        logging.info("Turn: %d", i)
        isReward = True
        isFailed = Play()
        if not isFailed:    #正常跳出才要去按Finish
            isReward = ClickFinish()    # 檢查有沒有獎賞
        if isFailed:    #打失敗了, 重新打這關而且不計次數
            i -= 1
        if configObj.getPlayMode() == PlayModeType.ONE_STAGE:
            if not isReward:           #沒有獎勵則強制換關
                zero_reward_count += 1 
                if zero_reward_count == 3: #連刷三次沒有獎勵則跳出
                    break
                ChangeStage(10) 
            else:                      #有獎勵
                ChangeStage(i)         #檢查看是否滿10次需要換關   

if __name__ == "__main__":
    main()
  