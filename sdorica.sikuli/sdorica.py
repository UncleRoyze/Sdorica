# -*- coding: UTF-8 -*-
from java.awt import Color
from java.awt import Robot
import datetime
from time import time
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
    ini_mode = int(configObj.config.get("setting", "mode"))
    modes = ModeFactory.GenModeInfo()
    algos = AlgoFactory.GenAlgoInfo()
    ini_turn = configObj.config.get("setting", "turn")
    ini_algo = int(configObj.config.get("setting", "algo"))
    ini_designated_hour = configObj.config.get("setting", "designated_hour")

    msg = "Current setting: \n Mode: %s \n Algo: %s \n Turns: %s \n Designated Time: %s \n\n Use this setting?" \
           % (modes[ini_mode], algos[ini_algo], ini_turn, ini_designated_hour)
    answer = popAsk(msg)
    if answer:
        return

    selected_mode = select("Please select mode", options = modes, default = modes[ini_mode])
    playmode = ModeFactory.GetModeIndex(selected_mode)
    if playmode < 0:
        exit(1)
    configObj.config.set("setting", "mode", str(playmode))
    
    selected_algo = select("Please select algorithm", options = algos, default = algos[ini_algo])
    algorithm = AlgoFactory.GetAlgoIndex(selected_algo)
    if algorithm < 0:
        exit(1)
    configObj.config.set("setting", "algo", str(algorithm))

    turn = int(input("The max turns?", ini_turn))
    if turn < 0:
        exit
    configObj.config.set("setting", "turn", str(turn))

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
    wait(timedelta.seconds + 300)

def EnterSdorica():
    app = exists("sdorica.png", 1)
    if app:
        click(app)
        wait(1)
    else:
        logging.debug("Cannot find Sdorica app")
        return
    app_title = exists("app_title.png", 30)
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
  
