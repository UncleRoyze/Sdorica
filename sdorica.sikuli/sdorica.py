# -*- coding: UTF-8 -*-
from java.awt import Color
from java.awt import Robot
from time import time
import logging, sys
import AutoLvUp
reload(AutoLvUp)
import config
reload(config)
import PlayAlgo
reload(PlayAlgo)
import ModeClass
reload(ModeClass)

configObj = config.Configuration()
logging.basicConfig(format='%(asctime)s:%(message)s',stream=sys.stdout, level=logging.DEBUG)

def StartAsking():
    ini_mode = int(configObj.config.get("setting", "mode"))
    #modes = ("Farm", "Auto Lelve Up", "Material", "Auto Farm")
    modes = ModeFactory.GenModeInfo()
    algos = AlgoFactory.GenAlgoInfo()
    ini_turn = configObj.config.get("setting", "turn")
    ini_algo = int(configObj.config.get("setting", "algo"))
   
    msg = "Current setting: \n Mode: %s \n Algo: %s \n Max Turn: %s  \n\n Use this setting?" \
           % (modes[ini_mode], algos[ini_algo], ini_turn)
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

    #write ini
    configObj.writeConfig()

def main():
    StartAsking()
    playMode = ModeFactory.GenMode(configObj.getPlayMode())
    playMode.Run()

if __name__ == "__main__":
    main()
  
