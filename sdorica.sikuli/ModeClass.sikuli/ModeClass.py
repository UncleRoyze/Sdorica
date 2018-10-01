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
        self.dragLeftMore = topLeft.offset(49, 450)
        self.dragRight = topLeft.offset(877, 450)
        self.dragTop = topLeft.offset(790, 61)
        self.dragBottom = topLeft.offset(790, 482)
         
    #角色選單拉到最右邊
    def ToRightEnd(self, dragTimes):       
        for i in range(dragTimes):
            Settings.MoveMouseDelay = 0.1
            Settings.DelayBeforeDrop = 0
            dragDrop(self.dragRight, self.dragLeft)
            #稍微拉左點
            Settings.DelayBeforeDrop = 0.1
            dragDrop(self.dragLeft, Location(self.dragLeft.x+15,self.dragLeft.y))
            Settings.DelayBeforeDrop = 0
            wait(1)
    #角色選單拉到最左邊
    def ToLeftEnd(self, dragTimes):       
        for i in range(dragTimes):
            Settings.MoveMouseDelay = 0.1
            Settings.DelayBeforeDrop = 0
            dragDrop(self.dragLeft, self.dragRight)
            wait(1)
    #角色選單拉往左, 一次拉一整排五位位置都正好換掉
    def ToLeft(self):
        Settings.MoveMouseDelay = 0.001
        drag(self.dragLeft)
        Settings.MoveMouseDelay = 1.5
        dropAt(self.dragRightMore)
        Settings.MoveMouseDelay = 0.001
        hover(self.dragLeft)
        
    #角色選單拉往右, 一次拉一整排五位位置都正好換掉
    def ToDown(self):
        Settings.MoveMouseDelay = 0.001
        drag(self.dragBottom)
        Settings.MoveMouseDelay = 1.5
        dropAt(self.dragTop)
        Settings.MoveMouseDelay = 0.001

    def ToRight(self):
        Settings.MoveMouseDelay = 0.001
        drag(self.dragRight)
        Settings.MoveMouseDelay = 1.5
        dropAt(self.dragLeftMore)
        Settings.MoveMouseDelay = 0.001
        hover(self.dragRight)
        
class ModeFactory():
    FARM = 0
    AUTO_LV_UP = 1
    MATERIAL = 2
    QUEST = 3
    THURSDAY_4 = 4
    FRIDAY_3 = 5
    TEMP = 6
    MODE_DICT = {FARM: "Farm",
                 AUTO_LV_UP: "Auto Lelve Up",
                 MATERIAL : "Material",
                 QUEST : "Quest",
                 THURSDAY_4 : "Thursday 4",
                 FRIDAY_3 : "Friday 3",
                 TEMP : "TEMP" }

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
        elif choice == ModeFactory.TEMP:
            return TempaMode()
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
        #self.Algo = AlgoFactory.JIN2_ALGO
        self.one_stage_count = 0

    def InitParameter(self):
        self.Failed = False
        self.Reward = True
        self.quit_play = False

    def Run(self):
        if not IsNightGodRunning():
            return
        self.InputSetting()
        self.SelectStage()
        for self.TurnCount in range(configObj.getTurns()):
            if not IsNightGodRunning(): break
            if self.Quit: break
            logging.info("Turn: %d", self.TurnCount)
            self.InitParameter()
            if self.Quit: break
            self.IntoStage()
            if self.Quit: break
            self.SelectFighter()
            if self.Quit: break
            self.SelectBrainman()
            if self.Quit: break
            self.IntoPlay()
            if self.Quit: break
            self.Playing()
            if self.Quit: break
            self.LeavePlay()
            if self.Quit: break
            self.WaitToMenu()
            if self.Quit: break
            self.ToNextStage()
            if self.Quit: break
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
        if exists(Pattern("clock.png").similar(0.95) , 0.001):   
            logging.debug("IsInPlaying")
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
        start_exists = exists(start, 0.001)
        if start_exists:
            wait(1)
            click(start_exists)

    def SelectFighter(self):
        logging.debug("SelectFighter")
        if self.IsInPlaying():
            return
        for i in range(5000):
            if self.IsInStage():
                break
        if not self.IsInStage():
            return
        Settings.MoveMouseDelay = 0.01
        if self.Algo == AlgoFactory.JIN2_ALGO or  self.Algo == AlgoFactory.NO1_ALGO or self.Algo == AlgoFactory.ONE_TO_TEN_ALGO:
            if exists(Pattern("team_2.png").similar(0.90), 1):
                click(Pattern("team_2.png").similar(0.90))
        elif self.Algo == AlgoFactory.NOLVA_ALGO or self.Algo == AlgoFactory.NO2_ALGO:
            if exists(Pattern("team3.png").similar(0.90), 1):
                click(Pattern("team3.png").similar(0.90))

    def SelectBrainman(self):
        logging.debug("SelectBrainman")
        if not self.IsInStage():
            return
            
        def _findBrainman():
            Settings.MoveMouseDelay = 0.1
            dragFrom = friendSlotCenter.offset(290, -430)
            dragTo = friendSlotCenter.offset(190, -430)
            
            selectCenter = None
            trueFriendFound = False
            
            with MouseDragHandler(dragFrom, dragTo):
                matches = findAnyList(configObj.friends + configObj.brainmen)

            if matches:
                for match in matches:
                    matchCenter = match.getCenter()
                    if match.getIndex() > len(configObj.friends) - 1:
                        reg = Region(matchCenter.x - 60, matchCenter.y - 80, 120, 30)
                        if reg.exists("using.png"):
                            # 好用的參謀跟自己隊伍的角色相同，只好不選他了
                            continue
                        selectCenter = matchCenter  # 沒找到朋友的參謀，選其他好用的
                        break
                    else:
                        reg = Region(matchCenter.x - 60, matchCenter.y - 10, 120, 160)
                        if reg.exists("using.png"):
                            # 好友的參謀跟自己隊伍的角色相同，只好不選他了
                            continue
                        selectCenter = reg.getCenter()
                        trueFriendFound = True
                        break
            if selectCenter:
                click(selectCenter)
            return trueFriendFound
            
        friendSlot = exists(Pattern("SelectFriend.png").similar(0.95), 0.001)
        if not friendSlot:
            return
        click(friendSlot)
        friendSlotCenter = friendSlot.getCenter()
        _findBrainman()

    def IntoPlay(self):
        logging.debug("IntoPlay")
        if not self.IsInStage():
            return
        start = "gotofight.png"
        if exists(start,10):
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
        #logging.debug("CheckFailed")
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
        
    def PlayDrag(self, clock, sub_stage):
        logging.debug("PlayDrag")
        Settings.MoveMouseDelay = 0.1
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
            status = playAlgo.Play(clock, sub_stage, turn)
            if status == -1: #跑結束
                self.quit_play = True
                return 0
            elif status == 0: #沒有點擊
                continue
            wait(1)
            turn += 1
        return 1


    def Playing(self):
        logging.debug("Playing")
        clock = exists(Pattern("clock.png").similar(0.90) , 1)
        sub_stage = 0
        while clock:
            sub_stage += 1
            self.DragForward(clock) 
            if not self.PlayDrag(clock, sub_stage):  #跑結束
                break
            self.CheckFailed()            #檢查有無輸
            if self.Failed:
                break
            clock = exists(Pattern("clock.png").similar(0.90) , 0.001) #檢查現在是不是還在關卡裡
            
    def _quit_play(self):
        clock = exists(Pattern("clock.png").similar(0.90) , 1)
        if clock:
            click(clock.getCenter().offset(-78,0))
            wait(1)
            click("ok_btn_quit.png")
        self.quit_play = False
        return
    
    def LeavePlay(self):
        logging.debug("LeavePlay")
        if self.Failed:
            return
        if self.quit_play == True:
            self._quit_play()
            #return
        Settings.MoveMouseDelay = 0.001
        for i in range(20):
            
            if exists(Pattern("finish_btn.png").similar(0.90), 1):
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
        else:
            self.ZeroRewardCount = 0            #重新計算
  
        for i in range(1000):    # 檢查按了按鈕之後有沒有真的結束
            finish_btn = exists(Pattern("finish_btn.png").similar(0.90), 0.001) 
            if finish_btn:
                click(finish_btn)
                wait(0.01)
            else:
                break
        

    def WaitToMenu(self): #等待回到選單
        logging.debug("WaitToMenu")
        start = "gotofight.png"
        if exists(start, 20):
            return

    def ToNextStage(self):
         return 0

class ChallengeMode(BasicMode):

    def InputSetting_backup(self):
        challenge_stage = input("Please enter challenge stage: (1~13)", str(configObj.getChallengeStage()))
        challenge_sub_stage = input("Please enter challenge sub stage: (1~5)", str(configObj.getChallengeSubStage()))
        configObj.setChallengeStage(challenge_stage)
        configObj.setChallengeSubStage(challenge_sub_stage)
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

        challenge_btn = exists("1538362880595.png", 0.001) 
        if challenge_btn:
            click(challenge_btn)
            wait(1)
        else:
            logging.debug("Cannot find challenge button, try to find the selected one.")
            
        challenge_btn_selected = exists("1538362847793.png", 0.001)
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
        
        played_stages = configObj.getChallengePlayedStages()
        scroll_times = challenge_count - played_stages
        if scroll_times < 0:  # we need to jump to previous page
            click(Pattern("previous_arrow.png").similar(0.85))
            for i in range(7):
                Settings.MoveMouseDelay = 0.1
                Settings.DelayBeforeDrop = 0   # scroll to bottom
                dragDrop(challenge_title.getCenter().offset(0, 640), challenge_title.getCenter().offset(0, 240))
            wait(1)
            # in case the cursor did not scroll to the bottom
            dragDrop(challenge_title.getCenter().offset(0, 440), challenge_title.getCenter().offset(0, 240))
            scroll_times = abs(scroll_times) - 1
            for i in range(scroll_times):
                dragDrop(challenge_title.getCenter().offset(0, 240), challenge_title.getCenter().offset(0, 440))

        else:  # normal case
            for i in range(7):
                Settings.MoveMouseDelay = 0.1
                Settings.DelayBeforeDrop = 0   # back to top
                dragDrop(challenge_title.getCenter().offset(0, 240), challenge_title.getCenter().offset(0, 640))
            wait(1)
            for i in range(scroll_times):
                dragDrop(challenge_title.getCenter().offset(0, 440), challenge_title.getCenter().offset(0, 240))


class FarmMode(ChallengeMode):
            
    def ChangeStage(self, isChange):
        self.one_stage_count += 1
        if self.one_stage_count > 9 or isChange:
            logging.debug("ChangeStage")
            self.one_stage_count = 0

            # Update played_stages in config
            played_stages = configObj.getChallengePlayedStages() + 1
            configObj.setChallengePlayedStages(played_stages)
            configObj.writeConfig()

            region_title = wait("stage_title_1.png", 10)
            sleep(2)
            if region_title:
                Settings.MoveMouseDelay = 0.1
                Settings.DelayBeforeDrop = 2
                dragDrop(region_title.getCenter().offset(0, 240), region_title.getCenter().offset(0, 440))
                Settings.MoveMouseDelay = 0.001 
                Settings.DelayBeforeDrop = 0

    def ToNextStage(self):
        logging.debug("ToNextStage")
        if self.Failed:
            return
        if not self.Reward:
            if self.ZeroRewardCount == 3:  # 連刷三次沒有獎勵則跳出
                # Reset played_stages in config
                configObj.setChallengePlayedStages(0)
                configObj.writeConfig()
                self.Quit = True
            else:
                self.ChangeStage(True)   #沒有獎勵則強制換關
        else:
            self.ChangeStage(False)      #檢查看是否滿10次需要換關   
            

class MaterialMode(BasicMode):

    def InputSetting(self):
        material_stage = input("Please enter stage:\n1.G Stone\n2.B Bear\n3.W Seed\n4.G Candlestick\n5.W Branches\n6.G Snake\n7.B Doll", str(configObj.getMaterialStage()))
        material_sub_stage = input("Please enter sub stage:", str(configObj.getMaterialSubStage()))
        configObj.setMaterialStage(material_stage)
        configObj.setMaterialSubStage(material_sub_stage)
        configObj.writeConfig()
        
    def SelectStage(self):
        self.MoveSpeed = 35
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
            Settings.MoveMouseDelay = 0.001  
            Settings.DelayBeforeDrop = 0

    def ActionDuringDrag(self, clock, dragFrom, dragTo):
        self.CollectMaterials(clock, dragFrom, dragTo)
        return
        
    def Playing(self):
        logging.debug("Playing")
        clock = exists(Pattern("clock.png").similar(0.90) , 0.001)
        sub_stage = 0
        while clock:
            sub_stage += 1
            self.CollectMaterials(clock, None, None)  # 距離起點很近的素材在移動後會來不及找到，所以在移動前先找一次
            self.DragForward(clock) 
            self.PlayDrag(clock, sub_stage)
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
        if exists(Pattern("quest_btn.png").similar(0.90),1):
            click(Pattern("quest_btn.png").similar(0.90))
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
            logging.debug("_leave_quest_page")
            wait(1)
            
    def _donate(self, money, blue):
        self._leave_quest_page()
        if not money and not blue:
            return 
        logging.debug("_donate")
        if exists(Pattern("guild_page_btn.png").similar(0.90), 10):
            click(Pattern("guild_page_btn.png").similar(0.90))
            wait(2)
        else:
            logging.debug("Cannot find guild button")
        if exists(Pattern("guild_quit_btn.png").similar(0.90), 0.001):
            click(Pattern("guild_quit_btn.png").similar(0.90))
            wait(2)
        else:
            logging.debug("Cannot find guild exit button")
        if exists(Pattern("guild_prestige.png").similar(0.90), 0.001):
            click(Pattern("guild_prestige.png").similar(0.90))
            wait(2)
        else:
            logging.debug("Cannot find prestige button")
        donate_btn = exists(Pattern("donate_btn.png").similar(0.80), 0.001)
        if not donate_btn:
            logging.debug("Cannot find donate button")
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
            for i in range(20):
                click(Pattern("donate_plus_btn.png").similar(0.90))
            click(Pattern("donate_ok_btn.png").similar(0.85), 1)
            wait(1)
            click(Pattern("donate_ok_btn.png").similar(0.85), 1)
            wait(1)
        #self._buy_guild_market_free_item()
        if exists(Pattern("journey_btn.png").similar(0.90), 0.001):
            click(Pattern("journey_btn.png").similar(0.90)) # back to main menu
            wait(1)
    def _buy_guild_market_free_item(self):
        market = exists(Pattern("guild_market.png").similar(0.90), 0.001)
        if market:
            click(market)
            wait(1)
            click(market.getCenter().offset(190,-240))
            wait(1)
            click(Pattern("max_btn.png").similar(0.90),1)
            wait(1)
            click(Pattern("donate_ok_btn.png").similar(0.85), 1) 
            wait(5)
    
    def _gulid_donate(self):
        logging.debug("_gulid_donate")
        self._click_quest_menu()
        self._click_quest_guild()
        money = False
        blue = False
        if exists(Pattern("quest_donate_money.png").similar(0.95), 0.001):
            money = True
            blue = True
        else:
            logging.debug("Did not found donate money")
#        if exists(Pattern("quest_donate_blue.png").similar(0.95), 0.001):
#            blue = True
        self._donate(money,blue)

    def _drag_quest_menu(self):
        quest_menu_title = exists(Pattern("quest_menu_title.png").similar(0.90), 0.001)
        if not quest_menu_title:
            return
        Settings.MoveMouseDelay = 0.1 
        dragDrop(quest_menu_title.getCenter().offset(0, 500), quest_menu_title.getCenter().offset(0, 100))
        wait(1)
        Settings.MoveMouseDelay = 0.001 
        
    def _get_quest_reward(self):
        if exists("get_reward_btn.png", 1):
            click("get_reward_btn.png")
            wait(1)
            
    def _select_quest(self):
        logging.debug("_select_quest")
        Settings.MoveMouseDelay = 0.1
        self._click_quest_menu()
        self._drag_quest_menu()
        if self._match_algo(configObj.quest_no1, AlgoFactory.NO1_ALGO):
            return
        if self._match_algo(configObj.quest_no2, AlgoFactory.NO2_ALGO):
            return
        if self._match_algo(configObj.quest_jin2, AlgoFactory.JIN2_ALGO):
            return
        if self._match_algo(configObj.quest_nolva, AlgoFactory.NOLVA_ALGO):
            return
        self._click_quest_guild()
        self._drag_quest_menu()

        if self._match_algo(configObj.quest_1to10, AlgoFactory.ONE_TO_TEN_ALGO):
            return
        if self._match_algo(configObj.quest_no1, AlgoFactory.NO1_ALGO):
            return
        if self._match_algo(configObj.quest_nolva, AlgoFactory.NOLVA_ALGO):
            return
        if self._match_algo(configObj.quest_jin2, AlgoFactory.JIN2_ALGO):
            return
        

        self.quest_done = True #解完任務了
        self._leave_quest_page()
        self._to_event_stage()

    def _match_algo(self, imgs, algo):
        matches = findAnyList(imgs)
        if matches:
            for match in matches:
                click(match)
                self.Algo = algo
                return True
        return False
    
    def _back_to_main_menu(self):
        logging.debug("_back_to_main_menu")
        for i in range(10):
            if exists(Pattern("news.png").similar(0.80), 0.001):
                wait(1)
                return
            elif exists("back_button.png", 0.001):
                click("back_button.png")
                wait(1)
            elif exists(Pattern("ad_cancel.png").similar(0.90), 0.001):
                click(Pattern("ad_cancel.png").similar(0.90))
                wait(1)
                
    def SelectStage(self):
        logging.debug("SelectStage")
        Settings.MoveMouseDelay = 0.1
        self._back_to_main_menu()
        self._gulid_donate()
        self._select_quest()
        return

    def _to_event_stage(self):
        logging.debug("to_event_stage")
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
            if exists(Pattern("1536627662878.png").similar(0.90), 1):
                self._back_to_main_menu()
                self.Quit = True
                return
            for i in range(2):
                Settings.MoveMouseDelay = 0.1
                Settings.DelayBeforeDrop = 0   # back to top
                dragDrop(event_title.getCenter().offset(0, 240), event_title.getCenter().offset(0, 640))
            wait(1)
            Settings.MoveMouseDelay = 0.1
            Settings.DelayBeforeDrop = 2
            for i in range(6):
                dragDrop(event_title.getCenter().offset(0, 440), event_title.getCenter().offset(0, 240))
                if exists(Pattern("money_event.png").similar(0.95),0.001):
                    break
            Settings.MoveMouseDelay = 0.001 
            Settings.DelayBeforeDrop = 0
                
    def ToNextStage(self):
        logging.debug("ToNextStage")
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
    

class Friday3Mode(BasicMode):

    def ActionDuringDrag(self, clock, dragFrom, dragTo):
        logging.debug("ActionDuringDrag")
        #region = Region(clock.x-130, clock.y-47, 1280, 720)
        #if not region.exists(Pattern("1532668283484.png").similar(0.95),0.001):
        #    return 
    
        #with MouseDragHandler(dragFrom, dragTo, True):
            #click(Pattern("1532668283484.png").similar(0.95))
            #click("ok_btn_buff.png")
        
    def SelectFighter(self):
        self.Algo = AlgoFactory.FRIDAY3_ALGO
        for i in range(5000):
            if self.IsInStage():
                break
        if not self.IsInStage():
            return
        bar = DragCharacterBar()
        start =  exists("gotofight.png", 30)
        if not start:
            exit
        if exists(Pattern("lv60.png").similar(0.80),0.001): #有紀錄的隊伍了
            return
        click(start.getCenter().offset(-600,-70))
        click("1536301234259.png")
        click(Pattern("skin_arrow.png").similar(0.90))
        click(start.getCenter().offset(-800,-70))
        click("nolva.png")
        click(Pattern("skin_arrow.png").similar(0.85))
        click(start.getCenter().offset(-1000,-70))
        click("puji.png")

        click(Pattern("skin_arrow.png").similar(0.85))
        click(start.getCenter().offset(-930,180))
        wait(1)
        for i in range(5):
            if exists(Pattern("1536301266208.png").similar(0.88),0.001):
                click(Pattern("1536301266208.png").similar(0.88))
                click(Pattern("skin_arrow.png").similar(0.85))
                break
            bar.ToDown()

    def SelectBrainman(self):
        return

class TempaMode(BasicMode):
    
    def SelectBrainman(self):
        return

    def ActionDuringDrag(self, clock, dragFrom, dragTo):
        logging.debug("ActionDuringDrag")
        #region = Region(clock.x-130, clock.y-47, 1280, 720)
        #if not region.exists(Pattern("1537344105808.png").similar(0.95)):
        #    return 
    
        #with MouseDragHandler(dragFrom, dragTo, True):
        #    click(Pattern("1537344105808.png").similar(0.95))
        #    click("ok_btn_buff.png")
            
    def SelectFighter(self):
        logging.debug("SelectFighter-TEMP")
        #self.Algo = AlgoFactory.TEMP_ALGO
        if self.IsInPlaying():
            return
        for i in range(1000):
            if self.IsInStage():
                break
        if not self.IsInStage():
            return

        bar = DragCharacterBar()
        start =  exists("gotofight.png", 30)
        if not start:
            exit
        if exists(Pattern("lv60.png").similar(0.80),0.001): #有紀錄的隊伍了
            return
        click(start.getCenter().offset(-600,-70))
        click("1536301234259.png")
        click(Pattern("skin_arrow.png").similar(0.90))
        click(start.getCenter().offset(-800,-70))
        click("nolva.png")
        click(Pattern("skin_arrow.png").similar(0.85))
        click(start.getCenter().offset(-1000,-70))
        click("puji.png")

        click(Pattern("skin_arrow.png").similar(0.85))
        click(start.getCenter().offset(-930,180))
        wait(1)
        for i in range(5):
            if exists(Pattern("1536301266208.png").similar(0.88),0.001):
                click(Pattern("1536301266208.png").similar(0.88))
                click(Pattern("skin_arrow.png").similar(0.85))
                break
            bar.ToDown()
