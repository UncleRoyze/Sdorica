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


def main():
    StartAsking()
    playMode = ModeFactory.GenMode(configObj.getPlayMode())
    start_time = time()
    playMode.Run()
    time_taken = time() - start_time  # time_taken is in seconds
    popup("Duration: %d min." % (time_taken / 60))
        

if __name__ == "__main__":
    main()
  
