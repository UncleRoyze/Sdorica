# -*- coding: UTF-8 -*-

#自動選擇白位、金位、參謀裡面等級不夠的角色出陣來練等
#參謀裡面只選黑位, 用諾瓦1帶3鍊等

import ModeClass
reload(ModeClass)
from ModeClass import BasicMode, ChallengeMode

class AutoLvUpMode(ChallengeMode):

    def InputSetting():
        super(self.__class__, self).InputSetting()
        ini_target_lv = configObj.config.get("setting", "target_lv")
        target_lv = int(input("Please enter your targeted level:", ini_target_lv))
        configObj.config.set("setting", "target_lv", str(target_lv))
        #write ini
        configObj.writeConfig()
        
    def SelectFighter(self):
        SelectLowLevelCharacter(configObj.target_lv)
        
def SelectLowLevelCharacter(target_lv):
    logging.debug("SelectLowLevelCharacter")
    TARGET_LV_TITLE = [Pattern] * 61
    TARGET_LV_SMALL = [Pattern] * 61
    TARGET_LV_TITLE[55] = Pattern("lv55_title.png").similar(0.85)
    TARGET_LV_TITLE[57] = Pattern("lv57_title.png").similar(0.90)
    TARGET_LV_TITLE[58] = Pattern("lv58_title.png").similar(0.85)
    TARGET_LV_TITLE[59] = Pattern("lv59_title.png").similar(0.85)
    TARGET_LV_SMALL[55] = Pattern("lv55_small.png").similar(0.90)
    TARGET_LV_SMALL[57] = Pattern("lv57_small.png").similar(0.90)
    TARGET_LV_SMALL[58] = Pattern("lv58_small.png").similar(0.90)
    TARGET_LV_SMALL[59] = Pattern("lv59_small.png").similar(0.90)
    topLeft = exists(Pattern("back_button-2.png").targetOffset(460,0),0.001).getCenter()
    bar = DragCharacterBar()
   
    #選擇等級不夠的角色出戰     
    def _SelectCharacter():
        logging.debug("_SelectCharacter")
        bar.ToRightEnd(1)
        for j in range(4,-1,-1):    #檢查選單中的五個角色
            reg = Region()          #只檢查單一角色圖框的範圍
            reg.setROI(topLeft.x+115+j*160, topLeft.y+340, 190, 240) #從最右邊開始向左檢查
            if not reg.exists(TARGET_LV_SMALL[target_lv], 0.001):             #如果等級還沒練滿          
                if not reg.exists("using.png", 0.001):                #如果正在使用就不處理
                    reg.click(reg.getCenter())                       #如果沒在使用則點選該角色出陣
                return True
            else:            #由於遊戲裡越右邊的角色等級越低, 所以向左檢查到滿等級的角色時
                return False #代表再往左邊的角色也都會是滿等級的, 不需要再檢查
        return False
    #選擇等級不夠的黑位角色當作參謀   
    def _SelectSupport():
        logging.debug("_SelectSupport")
        reg = Region(topLeft.x+870, topLeft.y+260, 100, 75)
        if not reg.exists(Pattern("CharaterSelected_support.png").similar(0.80),0.001): #確認現在是否已經有角色當參謀, 並選到該參謀欄
            click(topLeft.offset(800,230))  #沒有選到參謀欄則click
        bar.ToRightEnd(3)
        for i in range(7):              #會滑動角色選單七次
            for j in range(4,-1,-1):    #檢查選單中的五個角色圖框
                reg = Region(topLeft.x+115+j*160, topLeft.y+340, 190, 240)  #從最右邊開始向左檢查
                if not reg.exists(Pattern("black_icon.png").similar(0.65), 0.001):    #跳過不是黑位的角色
                    continue
                if not reg.exists(TARGET_LV_SMALL[target_lv], 0.001):  #如果等級還沒練滿 
                    if not reg.exists("using.png", 0.001):     #如果正在使用就不處理
                        reg.click(reg.getCenter())            #如果沒在使用則點選該角色出陣
                    return True
                else:                     #由於遊戲裡越右邊的角色等級越低, 所以向左檢查到滿等級的角色時
                    return False          #代表再往左邊的角色也都會是滿等級的, 不需要再檢查
            bar.ToLeft()
        return False
    #檢查白位的角色是否滿等了需要換隻
    def _CheckWhite():
        logging.debug("_CheckWhite")
        reg = Region(topLeft.x+140, topLeft.y+65, 220, 300)
        if reg.exists(TARGET_LV_TITLE[target_lv], 1):    #白位現在出戰的角色已經滿等, 需要換角
            logging.debug("full lv")
            if not reg.exists(Pattern("CharaterSelected_white.png").similar(0.80),0.001): #確認是否已經選取白位
                click(topLeft.offset(200,215))  #沒有選取白位則click, 否則會進入出戰角色的頁面
            return True
        return False
    #檢查金位的角色是否滿等了需要換隻
    def _CheckYellow():
        logging.debug("_CheckYellow")
        reg = Region(topLeft.x+560, topLeft.y+65, 220, 300)
        if reg.exists(TARGET_LV_TITLE[target_lv], 1):    #金位現在出戰的角色已經滿等, 需要換角
            if not reg.exists(Pattern("CharaterSelected_gold.png").similar(0.80),0.001):  #確認是否已經選取金位
                click(topLeft.offset(610,215))  #沒有選取金位則click, 否則會進入出戰角色的頁面
            return True
        return False
    
    if _CheckWhite():
        _SelectCharacter()
    if _CheckYellow():
        _SelectCharacter()
    _SelectSupport()