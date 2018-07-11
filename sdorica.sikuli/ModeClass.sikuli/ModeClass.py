# -*- coding: UTF-8 -*-
from java.awt import Color
from java.awt import Robot
from time import time
import logging, sys
import config
reload(config)

configObj = config.Configuration()
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
    QUEST = 3
    THURSDAY_4 = 4
    FRIDAY_3 = 5
    MODE_DICT = {FARM: "Farm",
                 AUTO_LV_UP: "Auto Lelve Up",
                 MATERIAL : "Material",
                 QUEST : "Quest",
                 THURSDAY_4 : "Thursday 4",
                 FRIDAY_3 : "Friday 3"}

    @staticmethod
    def GenMode(choice):
        if choice == ModeFactory.FARM:
            return FarmMode()
        elif choice == ModeFactory.AUTO_LV_UP:
            return AutoLvUpMode()
        elif choice == ModeFactory.MATERIAL:
            return MaterialMode()
        elif choice == ModeFactory.QUEST:
            return QuestMode()
        elif choice == ModeFactory.THURSDAY_4:
            return Thursday4Mode()
        elif choice == ModeFactory.FRIDAY_3:
            return Friday3Mode()
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
        self.Algo = configObj.getAlgo()

    def InitParameter(self):
        self.Failed = False
        self.Reward = True
        
    def Run(self):
        #self.InputSetting()
        self.SelectStage()
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
            ok_btn = exists(Pattern("ok_btn_reward.png").similar(0.85), 0.001)
            if ok_btn:
                click(ok_btn)
                logging.debug("click ok button")
                wait(1)

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

    def SelectStage(self):
        logging.debug("self.SelectStage")
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
                            reg = Region(matchCenter.x - 65, matchCenter.y - 30, 140, 260)
                            if reg.exists("using.png"):
                                # 好友的參謀跟自己隊伍的角色相同，只好不選他了 
                                continue
                            selectCenter = reg.getCenter()
                            trueFriendFound = True
                            break
            click(selectCenter)
            return trueFriendFound
            
        friendSlot = exists(Pattern("SelectFriend.png").similar(0.90), 0.001)
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
            ok_btn = exists("ok_btn_1.png", 0.001)
            if ok_btn:    #如果跳出網路不好的圖示, 點擊OK
                    click(ok_btn)
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
        region = Region(clock.x+170, clock.y+430, 650, 200)
        if region.exists(Pattern("soul.png").similar(0.80),0.001) or region.exists(Pattern("soul_dead.png").similar(0.80),0.001): # 判斷魂盤
            return True
        else:
            region = Region(clock.x-70, clock.y+270, 170, 130)  # 判斷角色icon
            if region.exists(Pattern("white_icon.png").similar(0.95),0.001) or region.exists(Pattern("black_icon.png").similar(0.95),0.001) or region.exists(Pattern("gold_icon.png").similar(0.95),0.001):
                return True
            #logging.debug("no soul board")
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
                self.ActionDuringDrag(clock, dragFrom, dragTo)
                clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
                if not clock:
                    break
                end_time = time()
                time_taken = end_time - start_time # time_taken is in seconds
                if(time_taken >= 30): # not found
                    break            #exit while not exists
                
    def ActionDuringDrag(self, clock, dragFrom, dragTo):
        return
        
    def PlayDrag(self, clock):
        logging.debug("PlayDrag")
        if not clock:
            return 0
        turn = 0    
        playAlgo = AlgoFactory.GenAlgo(self.Algo,clock)
        while True:
            if not self.InSoulBoard(clock):
                break
            status = playAlgo.GetDotBoard(clock)
            if status == -1: #沒找到棋盤
                break
            elif status == 0: #敵人攻擊中, 棋盤辨識不出來
                continue
            #click(clock.getCenter().offset(60,480)) #點擊自己的參謀
            #click(clock.getCenter().offset(970,480)) #點擊公會的參謀
            status = playAlgo.Play(turn, clock)
            if status == -1: #跑結束
                return 0
            elif status == 0: #沒有點擊
                continue
            wait(1)
            turn += 1
        return 1
    
    def Playing(self):
        logging.debug("Playing")
        clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
        while clock:
            self.DragForward(clock) 
            if not self.PlayDrag(clock):  #跑結束
                break
            self.CheckFailed()            #檢查有無輸
            if self.Failed:
                break
            clock = exists(Pattern("clock.png").similar(0.90) , 0.001) #檢查現在是不是還在關卡裡

    def LeavePlay(self):
        logging.debug("LeavePlay")
        if self.Failed:
            return
        Settings.MoveMouseDelay = 0.1
        for i in range(30):
            
            if exists(Pattern("finish_button.png").similar(0.80), 1):
                break
            if exists("network_lost.png",0.001):# 檢查網路是否不穩
                click(Pattern("network_lost.png").targetOffset(0,140))       # 有網路不穩則點擊後跳出
                i = 60
                continue 
            if exists("gotofight.png", 0.001): #回到主畫面了
                return
        
        if exists(Pattern("zero_money.png").exact(), 2):    #沒有庫倫了
            self.Reward = False
            self.ZeroRewardCount += 1
            logging.debug("zero reward")
            wait(1)
        click(Pattern("finish_button.png").similar(0.80).targetOffset(32,0))

    def WaitToMenu(self): #等待回到選單
        logging.debug("WaitToMenu")
        start = "gotofight.png" 
        if exists(start, 20):
            wait(3)

    def ToNextStage(self):
         return 0

class ChallengeMode(BasicMode):

    def InputSetting(self):
        ini_challenge_stage = configObj.config.get("challenge", "stage")
        ini_challenge_sub_stage = configObj.config.get("challenge", "sub_stage")
        challenge_stage = int(input("Please enter challenge stage: (1~13)", ini_challenge_stage))
        challenge_sub_stage = int(input("Please enter challenge sub stage: (1~5)", ini_challenge_sub_stage))
        configObj.config.set("challenge", "stage", str(challenge_stage))
        configObj.config.set("challenge", "sub_stage", str(challenge_sub_stage))
        #write ini
        configObj.writeConfig()

    def SelectStage(self):
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

        challenge_btn = exists("challenge_btn.png", 0.001) 
        if challenge_btn:
            click(challenge_btn)
            wait(1)
        else:
            logging.debug("Cannot find challenge button, try to find the selected one.")
            
        challenge_btn_selected = exists("challenge_btn_selected.png", 0.001)
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


class FarmMode(ChallengeMode):

    def SelectFighter(self):
        if exists(Pattern("team_2.png").similar(0.90), 1):
            click(Pattern("team_2.png").similar(0.90))
            
    def ChangeStage(self, i):
        if i % 10 == 0 and i != 0:
            logging.debug("ChangeStage")
            region_title = wait("stage_title_1.png", 10)
            if region_title:
                dragDrop(region_title.getCenter().offset(0, 240), region_title.getCenter().offset(0, 440))

    def ToNextStage(self):
        logging.debug("ToNextStage")
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
        #write ini
        configObj.writeConfig()
        
    def SelectStage(self):
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

    def ActionDuringDrag(self, clock, dragFrom, dragTo):
        self.CollectMaterials(clock, dragFrom, dragTo)
        return
        
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

class QuestMode(BasicMode):

    quest_done = False
    event_count = 0
    def _click_quest_menu(self):
        if exists("quest_btn.png",0.001):
            click("quest_btn.png")
            wait(1)
        else:
            logging.debug("Cannot find quest button")

    def _click_quest_guild(self):
        if exists(Pattern("quest_guild.png").similar(0.90),5):
            click(Pattern("quest_guild.png").similar(0.90))
            wait(1)
        else:
            logging.debug("Cannot find quest guild button")

    def _leave_quest_page(self):
        if exists(Pattern("quest_leave_btn.png").similar(0.90), 0.001):
            click(Pattern("quest_leave_btn.png").similar(0.90))
            wait(1)
            
    def _donate(self, money, blue):
        if not money and not blue:
            self._leave_quest_page()
            return 
        self._leave_quest_page()
        if exists(Pattern("guild_page_btn.png").similar(0.90), 0.001):
            click(Pattern("guild_page_btn.png").similar(0.90))
            wait(2)
        if exists(Pattern("guild_quit_btn.png").similar(0.90), 0.001):
            click(Pattern("guild_quit_btn.png").similar(0.90))
            wait(2)
        if exists(Pattern("guild_prestige.png").similar(0.90), 0.001):
            click(Pattern("guild_prestige.png").similar(0.90))
            wait(2)
        donate_btn = exists(Pattern("donate_btn.png").similar(0.80), 0.001)
        if not donate_btn:
            return
        if money:
            click(donate_btn.getCenter().offset(0,-30))
            wait(1)
            for i in range(120):
                click(Pattern("donate_plus_btn-1.png").similar(0.90))
            click(Pattern("donate_ok_btn.png").similar(0.85), 1)
            wait(1)
            click(Pattern("donate_ok_btn.png").similar(0.85), 1)
            wait(1)
        if blue:
            click(donate_btn.getCenter().offset(0,30))
            for i in range(10):
                click(Pattern("donate_plus_btn.png").similar(0.90))
            click(Pattern("donate_ok_btn.png").similar(0.85), 1)
            wait(1)
            click(Pattern("donate_ok_btn.png").similar(0.85), 1)
            wait(1)
        if exists(Pattern("journey_btn.png").similar(0.90), 0.001):
            click(Pattern("journey_btn.png").similar(0.90)) # back to main menu
            
    def _gulid_donate(self):
        logging.debug("_gulid_donate")
        self._click_quest_menu()
        self._click_quest_guild()
        money = False
        blue = False
        if exists(Pattern("quest_donate_money.png").similar(0.95), 0.001):
            money = True
        else:
            logging.debug("Did not found donate money")
        if exists(Pattern("quest_donate_blue.png").similar(0.95), 0.001):
            blue = True
        self._donate(money,blue)

    def _drag_quest_menu(self):
        quest_menu_title = exists(Pattern("quest_menu_title.png").similar(0.90), 0.001)
        if not quest_menu_title:
            return
        dragDrop(quest_menu_title.getCenter().offset(0, 430), quest_menu_title.getCenter().offset(0, 215))
        
    def _get_quest_reward(self):
        if exists("get_reward_btn.png", 1):
            click("get_reward_btn.png")
            wait(1)
            
    def _select_quest(self):
        logging.debug("_select_quest")
        self._click_quest_menu()
        self._drag_quest_menu()
        if exists(Pattern("quest_20t.png").similar(0.95).targetOffset(30,0),0.001):
            click(Pattern("quest_20t.png").similar(0.95).targetOffset(30,0))
            self.Algo = AlgoFactory.JIN2_ALGO
            return
        if exists(Pattern("quest_treasure.png").similar(0.95).targetOffset(50,0),0.001):
            click(Pattern("quest_treasure.png").similar(0.95).targetOffset(50,0))
            self.Algo = AlgoFactory.JIN2_ALGO
            return
        self._click_quest_guild()
        self._drag_quest_menu()
        if exists(Pattern("quest_guild_lv4-0.png").similar(0.95),0.001):
            click(Pattern("quest_guild_lv4-0.png").similar(0.95))
            self.Algo = AlgoFactory.NOLVA_ALGO
            return
        if exists(Pattern("quest_guild_lv3.png").similar(0.95),0.001):
            click(Pattern("quest_guild_lv3.png").similar(0.95))
            self.Algo = AlgoFactory.NOLVA_ALGO
            return
        self.quest_done = True #解完任務了
        self._leave_quest_page()
        self._to_event_stage()

    def _back_to_main_menu(self):
        logging.debug("_back_to_main_menu")
        for i in range(10):
            if exists(Pattern("news.png").similar(0.80), 0.001):
                wait(1)
                return
            if exists("back_button.png", 0.001):
                click("back_button.png")
                wait(1)
                
    def SelectStage(self):
        logging.debug("SelectStage")
        self._back_to_main_menu()
        self._gulid_donate()
        self._select_quest()
        return

    def SelectFighter(self):
        if not self.IsInStage():
            return
        if self.Algo == AlgoFactory.JIN2_ALGO:
            if exists(Pattern("team_2.png").similar(0.90), 1):
                click(Pattern("team_2.png").similar(0.90))
        elif self.Algo == AlgoFactory.NOLVA_ALGO:
            if exists(Pattern("team3.png").similar(0.90), 1):
                click(Pattern("team3.png").similar(0.90))

    def _to_event_stage(self):
        self.Algo = AlgoFactory.JIN2_ALGO
        self.event_count += 1
        event_menu_btn = exists(Pattern("event_menu_page.png").similar(0.80), 0.001)
        if event_menu_btn:
            click(event_menu_btn)
            wait(1)
        event_menu_btn_selected = exists(Pattern("event_menu_btn_selected.png").similar(0.80), 0.001)
        if event_menu_btn_selected:
            click(event_menu_btn_selected)
            wait(1)
        event_title = exists(Pattern("event_title.png").similar(0.80), 1)
        if event_title:
            while not exists(Pattern("limit_event.png").similar(0.80), 0.001):
                click(Pattern("next_arrow.png").similar(0.85))
                wait(1)
            if exists(Pattern("left_zero.png").similar(0.90)):
                return
            for i in range(2):
                Settings.MoveMouseDelay = 0.1
                Settings.DelayBeforeDrop = 0   # back to top
                dragDrop(event_title.getCenter().offset(0, 240), event_title.getCenter().offset(0, 640))
            wait(1)
            Settings.MoveMouseDelay = 0.1
            Settings.DelayBeforeDrop = 2
            for i in range(2):
                dragDrop(event_title.getCenter().offset(0, 440), event_title.getCenter().offset(0, 240))
                
    def ToNextStage(self):
        self._back_to_main_menu()
        if not self.quest_done:
            self._select_quest()
        elif self.event_count < 2:
            self._to_event_stage()
        else:
            self.Quit = True

class Thursday4Mode(BasicMode):

    def ActionDuringDrag(self, clock, dragFrom, dragTo):
        logging.debug("ActionDuringDrag")
        region = Region(clock.x-130, clock.y-47, 1280, 720)
        if not region.exists(Pattern("buff2.png").similar(0.95),0.001):
            return 
    
        with MouseDragHandler(dragFrom, dragTo, True):
            click(Pattern("buff2.png").similar(0.95))
            click("ok_btn_buff.png")
        
    def SelectFighter(self):
        if not self.IsInStage():
            return
        bar = DragCharacterBar()
        start =  exists("gotofight.png", 30)
        if not start:
            exit
        if exists(Pattern("lv60.png").similar(0.80),0.001): #有紀錄的隊伍了
            return
        click(start.getCenter().offset(-936,-80))
        click(Pattern("Lisa_name.png").similar(0.90))
        click(start.getCenter().offset(-734,-80))
        click(Pattern("Ned_name.png").similar(0.90))
        click(Pattern("skin_arrow.png").similar(0.90))
        click(start.getCenter().offset(-526,-80))
        bar.ToRight()
        click(Pattern("jahan_name.png").similar(0.90))
        click(start.getCenter().offset(-344,-60))
        for i in range(5):
            if exists(Pattern("WestOmore_name.png").similar(0.90),0.001):
                click(Pattern("WestOmore_name.png").similar(0.90))
                break
            bar.ToRight()
        click(Pattern("WestOmore_name.png").similar(0.90))
        

    def SelectBrainman(self):
        return
    
    def LeavePlay(self):
        wait(1)
        clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
        if clock:
            click(clock.getCenter().offset(-78,0))
            wait(1)
            click("ok_btn_quit.png")
        return

class Friday3Mode(BasicMode):

    def ActionDuringDrag(self, clock, dragFrom, dragTo):
        logging.debug("ActionDuringDrag")
        region = Region(clock.x-130, clock.y-47, 1280, 720)
        if not region.exists(Pattern("buff2.png").similar(0.95),0.001):
            return 
    
        with MouseDragHandler(dragFrom, dragTo, True):
            click(Pattern("buff2.png").similar(0.95))
            click("ok_btn_buff.png")
        
    def SelectFighter(self):
        if not self.IsInStage():
            return
        bar = DragCharacterBar()
        start =  exists("gotofight.png", 30)
        if not start:
            exit
        if exists(Pattern("lv60.png").similar(0.80),0.001): #有紀錄的隊伍了
            return
       
        click(start.getCenter().offset(-734,-80))
        click(Pattern("Nolva_name.png").similar(0.90))
        click(Pattern("skin_arrow.png").similar(0.85))
        click(start.getCenter().offset(-526,-80))
        bar.ToRight()
        click(Pattern("Delan_name.png").similar(0.85))
        click(Pattern("skin_arrow.png").similar(0.85))
        click(start.getCenter().offset(-936,-80))
        click(Pattern("WestOmore_name.png").similar(0.90))
        click(start.getCenter().offset(-344,-60))
        for i in range(5):
            if exists(Pattern("jahan_name.png").similar(0.90),0.001):
                click(Pattern("jahan_name.png").similar(0.90))
                break
            bar.ToRight()

    def SelectBrainman(self):
        return

    def LeavePlay(self):
        wait(1)
        clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
        if clock:
            click(clock.getCenter().offset(-78,0))
            wait(1)
            click("ok_btn_quit.png")
        return
    
