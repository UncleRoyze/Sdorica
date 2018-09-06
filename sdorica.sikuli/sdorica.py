# -*- coding: UTF-8 -*-
from java.awt import Color
from java.awt import Robot
import datetime
from time import time
import os
import logging, sys
import config
reload(config)
import PlayAlgo
reload(PlayAlgo)
from PlayAlgo import AlgoFactory
import ModeClass
reload(ModeClass)

configObj = config.Configuration()

logging.basicConfig(format='%(asctime)s:%(message)s',stream=sys.stdout, level=logging.DEBUG)

def StartAsking():
    modes = ModeFactory.GenModeInfo()
    algos = AlgoFactory.GenAlgoInfo()
    ini_mode = 0
    ini_turn = 1000
    ini_algo = 0
    ini_designated_hour = -1
    try:
        ini_mode = configObj.getPlayMode()
        ini_turn = configObj.getTurns()
        ini_algo = configObj.getAlgo()
        ini_designated_hour = configObj.getDesignatedHour()
    except:
        logging.debug("cannot read config file")

    msg = "Current setting: \n Mode: %s \n Algo: %s \n Turns: %s \n Designated Time: %s \n\n Use this setting?" \
           % (modes[ini_mode], algos[ini_algo], ini_turn, ini_designated_hour)
    answer = popAsk(msg)
    if answer:
        return

    selected_mode = select("Please select mode", options = modes, default = modes[ini_mode])
    playmode = ModeFactory.GetModeIndex(selected_mode)
    if playmode < 0:
        exit(1)
    configObj.setPlayMode(playmode)
    
    selected_algo = select("Please select algorithm", options = algos, default = algos[ini_algo])
    algorithm = AlgoFactory.GetAlgoIndex(selected_algo)
    if algorithm < 0:
        exit(1)
    configObj.setAlgo(algorithm)

    turn = int(input("The max turns?", str(ini_turn)))
    if turn < 0:
        exit
    configObj.setTurns(turn)

    #designated_hour = int(input("Please enter your designated time in hour (0~23)\n(-1 mean to run this script right away)", str(ini_designated_hour)))
    start_time = ["-1","5","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
    designated_hour = int(select("Please enter your designated time in hour (0~23)\n(-1 mean to run this script right away)", options = start_time, default = str(ini_designated_hour)))
    if designated_hour not in range(0, 24):
        designated_hour = -1
    configObj.setDesignatedHour(designated_hour)

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
    wait(timedelta.seconds + 300)

def LaunchNightGod():
    wk_dir = getBundlePath()
    shortcut_path = wk_dir + "\sdorica.lnk"
    p = subprocess.Popen('start /B ' + shortcut_path + ' /WAIT', shell=True)
    p.wait()

def EnterSdorica():
    wait_time = 1
#    if(configObj.getDesignatedHour() <> -1):
#        LaunchNightGod()
#        wait_time = 300
    app = exists("sdorica.png", wait_time)
    if app:
        click(app)
        wait(1)
    else:
        logging.debug("Cannot find Sdorica app")
        return

    ok_btn = exists(Pattern("ok_btn_reward-1.png").similar(0.85), 60)
    if ok_btn:
        click(ok_btn)
        logging.debug("Update app")
        wait_time = 1200
    else:
        wait_time = 60
                
    app_title = exists("app_title.png", wait_time)
    if app_title:
        click(app_title)
        wait(1)
    else:
        logging.debug("Cannot find Sdorica title")
        return

    reward_btn = exists(Pattern("ok_btn_reward.png").similar(0.90), 60)
    if reward_btn:
        wait(1)
        click(reward_btn)
    else:
        logging.debug("Cannot find yesterday reward button")
    
    reward_btn = exists(Pattern("ok_btn_reward.png").similar(0.90), 30)
    if reward_btn:
        wait(1)
        click(reward_btn)
    else:
        logging.debug("Cannot find last week reward button")
        
    ad_cancel = exists(Pattern("ad_cancel.png").similar(0.90), 30)
    if ad_cancel:
        click(ad_cancel)
        wait(1)
    else:
        logging.debug("Cannot find advertisement cancel button")


def IsNightGodRunning():
    if programActive('NightGod - Sdorica'):
        return True
    else:
        logging.info("Did not found NightGod")
        return False

def programActive(vcProgram):
    searchResult = App.focus(vcProgram)
    if ("-1:" in str(searchResult)):
        return False
    else:
        return True
    
def main():
    StartAsking()
    WaitForDesignatedTime()
    EnterSdorica()
    start_time = time()
    if configObj.getPlayMode() == ModeFactory.FARM:
        playMode = ModeFactory.GenMode(ModeFactory.FARM)
        playMode.Run()
        playMode = ModeFactory.GenMode(ModeFactory.QUEST)
        playMode.Run()
    else:
        playMode = ModeFactory.GenMode(configObj.getPlayMode())
        playMode.Run()
    time_taken = time() - start_time  # time_taken is in seconds
    popup("Duration: %d min." % (time_taken / 60))
        

if __name__ == "__main__":
    main()
  
