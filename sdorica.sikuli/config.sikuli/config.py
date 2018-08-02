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
        self.friends = ["apollo.png", "roy.png", "hcm.png"]
        self.brainmen = [Pattern("delan_sp.png").similar(0.80), Pattern("Fatima_lv2.png").similar(0.80), Pattern("Sione_sp.png").similar(0.80), Pattern("Shirley_lv3.png").similar(0.80), Pattern("Shirley_lv2.png").similar(0.80), Pattern("YanBo_lv3.png").similar(0.80),Pattern("li_lv3.png").similar(0.80),Pattern("darkmoon_sp.png").similar(0.80)]
        self.materials = [[] for _ in range(10)]
        self.materials[1] = [Pattern("stone_1.png").similar(0.80), Pattern("stone_2.png").similar(0.80),Pattern("stone_3.png").similar(0.80)]
        self.materials[2] = [Pattern("tripod_1.png").similar(0.80), Pattern("tripod_2.png").similar(0.80), Pattern("tripod_3.png").similar(0.80), Pattern("tripod_4.png").similar(0.80), Pattern("tripod_5.png").similar(0.80)]
        self.materials[3] = [Pattern("flower00.png").similar(0.80),Pattern("flower01.png").similar(0.80),Pattern("flower02.png").similar(0.80),Pattern("flower03.png").similar(0.80),Pattern("flower04.png").similar(0.80)]
        self.materials[4] = [Pattern("bottle_0.png").similar(0.80),Pattern("bottle_1.png").similar(0.80)]
        self.materials[5] = [Pattern("fruit_1.png").similar(0.80), Pattern("fruit_2.png").similar(0.80), Pattern("fruit_3.png").similar(0.80), Pattern("fruit_4.png").similar(0.80), Pattern("fruit_5.png").similar(0.80)]
        self.materials[7] = [Pattern("masquerade_mask_1.png").similar(0.80), Pattern("masquerade_mask_2.png").similar(0.80), Pattern("masquerade_mask_3.png").similar(0.80), Pattern("masquerade_mask_4.png").similar(0.80), Pattern("masquerade_mask_5.png").similar(0.80)]
        self.material_stage_title = [Pattern("stage_title_r1.png").similar(0.90), Pattern("stage_title_r2.png").similar(0.90), Pattern("stage_title_r3.png").similar(0.90), Pattern("stage_title_r4.png").similar(0.90), Pattern("stage_title_r5.png").similar(0.90), Pattern("stage_title_r6.png").similar(0.90), Pattern("stage_title_r7.png").similar(0.90)]
        self.challenge_stage_title = [Pattern("challenge_title_t.png").similar(0.90), Pattern("challenge_title_c1.png").similar(0.95), Pattern("challenge_title_c2.png").similar(0.95), Pattern("challenge_title_c3.png").similar(0.95), Pattern("challenge_title_hero.png").similar(0.90)]
        self.quest_nolva = [Pattern("quest_guild_lv6-0.png").similar(0.95),Pattern("quest_guild_lv4-0.png").similar(0.95),Pattern("quest_guild_lv4-1.png").similar(0.95),Pattern("quest_guild_lv3-3.png").similar(0.95),Pattern("quest_guild_lv3-0.png").similar(0.95),Pattern("quest_guild_lv3-1.png").similar(0.95),Pattern("quest_guild_lv3-4.png").similar(0.95),Pattern("quest_guild_lv6-2.png").similar(0.95),Pattern("quest_guild_lv4-3.png").similar(0.95),Pattern("quest_lv8-2.png").similar(0.95),Pattern("quest_stone-2.png").similar(0.95)]
        self.quest_jin2 = [Pattern("quest_20t.png").similar(0.95),Pattern("quest_treasure-1.png").exact(),Pattern("quest_treasure-2.png").exact(),Pattern("quest_guild_lv6-1.png").similar(0.95),Pattern("quest_guild_lv4-2.png").similar(0.95),Pattern("quest_lv8-1.png").similar(0.96),Pattern("quest_lv8-3.png").similar(0.96),Pattern("quest_lv8-4.png").similar(0.96),Pattern("quest_lv8-5.png").similar(0.96),Pattern("quest_lv8-6.png").similar(0.96)]
        self.quest_no1 = [Pattern("quest_lv8-0.png").similar(0.95),Pattern("quest_stone.png").similar(0.95)]
        self.quest_1to10 = [Pattern("quest_lv6-2.png").similar(0.95)]
        
    def writeConfig(self):
        self.config.write(open(self.ini_path, 'wb'))

    def getTurns(self):
        return int(self.config.get("setting", "turn"))

    def setTurns(self, turn):
        self.config.set("setting", "turn", str(turn))

    def getPlayMode(self):
        return int(self.config.get("setting", "mode"))

    def setPlayMode(self, playmode):
        self.config.set("setting", "mode", str(playmode))

    def getMaterialStage(self):
        return int(self.config.get("material", "stage"))

    def setMaterialStage(self, material_stage):
        self.config.set("material", "stage", str(material_stage))

    def getMaterialSubStage(self):
        return int(self.config.get("material", "sub_stage"))

    def setMaterialSubStage(self, material_sub_stage):
        self.config.set("material", "sub_stage", str(material_sub_stage))

    def getChallengeStage(self):
        return int(self.config.get("challenge", "stage"))

    def setChallengeStage(self, challenge_stage):
        self.config.set("challenge", "stage", str(challenge_stage))

    def getChallengeSubStage(self):
        return int(self.config.get("challenge", "sub_stage"))

    def setChallengeSubStage(self, challenge_sub_stage):
        self.config.set("challenge", "sub_stage", str(challenge_sub_stage))

    def getChallengePlayedStages(self):
        return int(self.config.get("challenge", "played_stages"))

    def setChallengePlayedStages(self, played_stages):
        self.config.set("challenge", "played_stages", str(played_stages))        

    def getAlgo(self):
        return int(self.config.get("setting", "algo"))

    def setAlgo(self, algo):
        self.config.set("setting", "algo", str(algo))

    def getDesignatedHour(self):
        return int(self.config.get("setting", "designated_hour"))
    
    def setDesignatedHour(self, designated_hour):
        self.config.set("setting", "designated_hour", str(designated_hour))

    def getTargetLV(self):
        return int(self.config.get("setting", "target_lv"))

    def setTargetLV(self, target_lv):
        self.config.set("setting", "target_lv", str(target_lv))