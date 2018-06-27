# -*- coding: UTF-8 -*-
from java.awt import Color
from java.awt import Robot
from time import time
import logging, sys
import config
reload(config)

configObj = config.Configuration()
logging.basicConfig(format='%(asctime)s:%(message)s',stream=sys.stdout, level=logging.DEBUG)

class PlayModeType:
    FARM, AUTO_LV_UP, MATERIAL, AUTO_FARM = range(4)

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
        
    #角色選單拉往右, 一次拉一整排五位位置都正好換掉
    def ToRight(self):
        Settings.MoveMouseDelay = 0.001
        drag(self.dragRight)
        Settings.MoveMouseDelay = 1.5
        dropAt(self.dragLeft)
        Settings.MoveMouseDelay = 0.001
        hover(self.dragRight)
        
class ModeFactory():
    FARM = 0
    AUTO_LV_UP = 1
    MATERIAL = 2
    AUTO_FARM = 3
    MODE_DICT = {FARM: "Farm",
                 AUTO_LV_UP: "Auto Lelve Up",
                 MATERIAL : "Material",
                 AUTO_FARM : "Auto Farm"}

    @staticmethod
    def GenMode(choice):
        if choice == ModeFactory.FARM:
            return FarmMode()
        elif choice == ModeFactory.AUTO_LV_UP:
            return AutoLvUpMode()
        elif choice == ModeFactory.MATERIAL:
            return MaterialMode()
        elif choice == ModeFactory.AUTO_FARM:
            return AutoFarmMode()
        else:
            return BasicMode()

    @staticmethod
    def GenModeInfo():
        dictlist = []
        for key, name in ModeFactory.MODE_DICT.iteritems():
            dictlist.append(name)
        return dictlist

    @staticmethod
    def GetModeIndex(search_name):
        for key, name in ModeFactory.MODE_DICT.iteritems():   
            if name == search_name:
                return key
        return -1

class BasicMode(object):
    
    def __init__(self):
        self.Failed = False
        self.Reward = True
        self.Quit = False
        self.TurnCount = 0
        self.ZeroRewardCount = 0
        self.MoveSpeed = 500

    def InitParameter(self):
        self.Failed = False
        self.Reward = True
        
    def Run(self):
        self.InputSetting()
        self.SelectStaringStage()
        for self.TurnCount in range(configObj.getTurns()):  
            logging.info("Turn: %d", self.TurnCount)
            self.InitParameter()
            self.IntoStage()
            self.SelectFighter()
            self.SelectBrainman()
            self.IntoPlay()
            self.Playing()
            self.LeavePlay()
            self.WaitToMenu()
            self.ToNextStage()
            if self.Quit:
                break

    # 是否在關卡選單內        
    def IsInStage(self):
        if exists(Pattern("Brainman.png").similar(0.90), 0.001):       
            return True
        else:
            return False
        
    # 是否在遊戲關卡內        
    def IsInPlaying(self):
        if exists(Pattern("clock.png").similar(0.90) , 0.001):       
            return True
        else:
            return False
        
    def InputSetting(self):
        logging.debug("InputSetting")
        return 0

    def SelectStaringStage(self):
        logging.debug("self.SelectStaringStage")
        if self.IsInPlaying() or self.IsInStage():
            return
        return 0

    def IntoStage(self):
        logging.debug("IntoStage")
        if self.IsInPlaying() or self.IsInStage():
            return
        Settings.MoveMouseDelay = 0.1
        start = "gotofight.png" 
        if exists(start, 0.001):
            click(start)
            wait(1)

    def SelectFighter(self):
        if not self.IsInStage():
            return
        return 0

    def SelectBrainman(self):
        logging.debug("SelectBrainman")
        if not self.IsInStage():
            return
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

    def IntoPlay(self):
        logging.debug("IntoPlay")
        if not self.IsInStage():
            return
        start = "gotofight.png" 
        wait(start)
        click(start)
        
        #等到看到有時鐘才代表進入關卡
        start_time = time()
        while not exists(Pattern("clock.png").similar(0.90), 0.001):              
            if exists("ok_btn_1.png", 0.001):    #如果跳出網路不好的圖示, 點擊OK
                    click("ok_btn_1.png")
            if(start_time - time()  >= 30): # not found
                break            #exit while not exists

    def CheckFailed(self):
        logging.debug("CheckFailed")
        Settings.MoveMouseDelay = 0.1
        if exists("lost_message.png", 0.001):
            click(Pattern("lost_message.png").targetOffset(0,130))
            wait(5)
            logging.debug("Failed")
            self.Failed = True

    def InSoulBoard(self, clock):
        region = Region(clock.x-70, clock.y+270, 170, 130)
        if exists(Pattern("white_icon.png").exact(),0.001) or exists(Pattern("black_icon.png").exact(),0.001) or exists(Pattern("gold_icon.png").exact(),0.001):
            return True
        else:
            return False

    def DragForward(self, clock):
        logging.debug("DragForward")
        if not clock:
            return
        start_time = time()
        dragFrom = clock.getCenter().offset(100,400)
        dragTo = Location(dragFrom.x+self.MoveSpeed, dragFrom.y)
        Settings.MoveMouseDelay = 0.5
    
        with MouseDragHandler(dragFrom, dragTo):
            while not self.InSoulBoard(clock):
                end_time = time()
                time_taken = end_time - start_time # time_taken is in seconds
                if(time_taken >= 30): # not found
                    break            #exit while not exists
            
    def PlayDrag(self, clock):
        logging.debug("PlayDrag")
        if not clock:
            return
        turn = 0
        playAlgo = AlgoFactory.GenAlgo(configObj.getAlgo(),clock)
        while True:
            status = playAlgo.GetDotBoard()
            if status == -1: #沒找到棋盤
                break
            elif status == 0: #敵人攻擊中, 棋盤辨識不出來
                continue
            #click(clock.getCenter().offset(60,480)) #點擊自己的參謀
            #click(clock.getCenter().offset(970,480)) #點擊公會的參謀
            playAlgo.Play(turn)
            wait(1)
            turn += 1
    
    def Playing(self):
        logging.debug("Playing")
        clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
        while clock:
            self.DragForward(clock) 
            self.PlayDrag(clock)
            self.CheckFailed()            #檢查有無輸
            if self.Failed:
                break
            clock = exists(Pattern("clock.png").similar(0.90) , 0.001) #檢查現在是不是還在關卡裡

    def LeavePlay(self):
        logging.debug("LeavePlay")
        if self.Failed:
            return
        Settings.MoveMouseDelay = 0.1
        for i in range(60):
            
            if exists(Pattern("finish_button.png").similar(0.80), 1):
                break
            if exists("network_lost.png",0.001):# 檢查網路是否不穩
                click(Pattern("network_lost.png").targetOffset(0,140))       # 有網路不穩則點擊後跳出
                return 
        
        if exists(Pattern("zero_money.png").exact(), 2):    #沒有庫倫了
            self.Reward = False
            self.ZeroRewardCount += 1
        click(Pattern("finish_button.png").similar(0.80).targetOffset(26,0))

    def WaitToMenu(self): #等待回到選單
        logging.debug("WaitToMenu")
        start = "gotofight.png" 
        if exists(start, 30):
            wait(3)

    def ToNextStage(self):
         return 0

class FarmMode(BasicMode):

    def ChangeStage(self, i):
        if i % 10 == 0 and i != 0:
            logging.debug("ChangeStage")
            region_title = wait("stage_title_1.png", 10)
            if region_title:
                dragDrop(region_title.getCenter().offset(0, 240), region_title.getCenter().offset(0, 440))

    def ToNextStage(self):
        if self.Failed:
            self.TurnCount -= 1
        if not self.Reward:
            if self.ZeroRewardCount == 3: #連刷三次沒有獎勵則跳出
                self.Quit = True
            else:
                self.ChangeStage(10)   #沒有獎勵則強制換關
        else:
            self.ChangeStage(self.TurnCount)      #檢查看是否滿10次需要換關   
            
class MaterialMode(BasicMode):

    def InputSetting(self):
        self.MoveSpeed = 35
        ini_stage = configObj.config.get("material", "stage")
        ini_sub_stage = configObj.config.get("material", "sub_stage")
        material_stage = int(input("Please enter stage:\n1.G Stone\n2.B Bear\n3.W Seed\n4.G Candlestick\n5.W Branches\n6.G Snake\n7.B Doll", ini_stage))
        material_sub_stage = int(input("Please enter sub stage:", ini_sub_stage))
        configObj.config.set("material", "stage", str(material_stage))
        configObj.config.set("material", "sub_stage", str(material_sub_stage))
        
    def SelectStaringStage(self):
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

    def DragForward(self, clock):
        logging.debug("DragForward")
        if not clock:
            return
        start_time = time()
        dragFrom = clock.getCenter().offset(100,400)
        dragTo = Location(dragFrom.x+self.MoveSpeed, dragFrom.y)
        Settings.MoveMouseDelay = 0.5
    
        with MouseDragHandler(dragFrom, dragTo):
            while not self.InSoulBoard():
                self.CollectMaterials(clock, dragFrom, dragTo)
                end_time = time()
                time_taken = end_time - start_time # time_taken is in seconds
                if(time_taken >= 30): # not found
                    break            #exit while not exists
                
    def Playing(self):
        logging.debug("Playing")
        clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
        while clock:
            self.CollectMaterials(clock, None, None)  # 距離起點很近的素材在移動後會來不及找到，所以在移動前先找一次
            self.DragForward(clock) 
            self.PlayDrag(clock)
            self.CheckFailed()            #檢查有無輸
            if self.Failed:
                break
            clock = exists(Pattern("clock.png").similar(0.90) , 0.001) #檢查現在是不是還在關卡裡
            
    def CollectMaterials(self, clock, dragFrom, dragTo):
        logging.debug("CollectMaterials")
    
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