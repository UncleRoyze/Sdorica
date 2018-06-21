# -*- coding: UTF-8 -*-
from sikuli import *
import ConfigParser
import os

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class Configuration(Singleton):

    def __init__(self):
        self._readConfig()
        self._initGlobalConfig()

    def _readConfig(self):
        self.config = ConfigParser.ConfigParser()
        # get the directory containing your running .sikuli
        self.ini_path = os.path.dirname(getBundlePath())
        #if self.iniPath not in sys.path: 
        #    sys.path.append(self.iniPath)
        self.ini_path = os.path.join(self.ini_path, "sdorica.sikuli", "config.ini")
        #read ini
        self.config.optionxform = str
        self.config.read(self.ini_path)

    def _initGlobalConfig(self):
        self.target_lv = 59
        self.friends = ["apollo.png", "roy.png", "hcm.png"]
        self.brainmen = ["delan_sp.png", "Fatima_lv2.png", "Sione_sp.png", "Shirley_lv3.png", "Shirley_lv2.png", "YanBo_lv3.png"]
        self.materials = [[] for _ in range(10)]
        self.materials[1] = [Pattern("stone_1.png").similar(0.80), Pattern("stone_2.png").similar(0.80),Pattern("stone_3.png").similar(0.80)]
        self.materials[2] = [Pattern("tripod_1.png").similar(0.80), Pattern("tripod_2.png").similar(0.80), Pattern("tripod_3.png").similar(0.80), Pattern("tripod_4.png").similar(0.80), Pattern("tripod_5.png").similar(0.80)]
        self.materials[3] = [Pattern("flower01.png").similar(0.80),Pattern("flower02.png").similar(0.80),Pattern("flower03.png").similar(0.80)]
        self.materials[4] = [Pattern("bottle_0.png").similar(0.80),Pattern("bottle_1.png").similar(0.80)]
        self.materials[5] = [Pattern("fruit_1.png").similar(0.80), Pattern("fruit_2.png").similar(0.80), Pattern("fruit_3.png").similar(0.80), Pattern("fruit_4.png").similar(0.80), Pattern("fruit_5.png").similar(0.80)]
        self.materials[7] = [Pattern("masquerade_mask_1.png").similar(0.80), Pattern("masquerade_mask_2.png").similar(0.80), Pattern("masquerade_mask_3.png").similar(0.80), Pattern("masquerade_mask_4.png").similar(0.80), Pattern("masquerade_mask_5.png").similar(0.80)]
        self.material_stage_title = [Pattern("stage_title_r1.png").similar(0.90), Pattern("stage_title_r2.png").similar(0.90), Pattern("stage_title_r3.png").similar(0.90), Pattern("stage_title_r4.png").similar(0.90), Pattern("stage_title_r5.png").similar(0.90), Pattern("stage_title_r6.png").similar(0.90), Pattern("stage_title_r7.png").similar(0.90)]

    def writeConfig(self):
        self.config.write(open(self.ini_path, 'wb'))

    def getTurns(self):
        return int(self.config.get("setting", "turn"))

    def getPlayMode(self):
        return int(self.config.get("setting", "mode")) - 1

    def getMaterialStage(self):
        return int(self.config.get("material", "stage"))

    def getMaterialSubStage(self):
        return int(self.config.get("material", "sub_stage"))

    def getAlgo(self):
        return int(self.config.get("setting", "algo"))
