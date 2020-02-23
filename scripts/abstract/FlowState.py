import bge
import copy
import os
from scripts.abstract.settings.DroneSettings import DroneSettings
from scripts.abstract.settings.RadioSettings import RadioSettings
from scripts.abstract.settings.GraphicsSettings import GraphicsSettings
logic = bge.logic

class FlowState:
    #the version of the save data format
    VERSION = "1.0.0"

    #game modes
    GAME_MODE_EDITOR = 0
    GAME_MODE_SINGLE_PLAYER = 1
    GAME_MODE_MULTIPLAYER = 2

    #view modes
    VIEW_MODE_MENU=0
    VIEW_MODE_PLAY=1

    #log levels
    LOG_LEVEL_DEBUG = 0
    LOG_LEVEL_INFO = 1
    LOG_LEVEL_ERROR = 2

    LOG_LEVEL = LOG_LEVEL_DEBUG

    def __init__(self):
        self.__logFile = os.path.join(str(logic.expandPath("//")),"flowstate.log") #remove once propper logging is implemented

        self.log("FlowState.init()")
        self._version = self.VERSION
        self._timeLimit = 3
        self._checkpoints = []
        self._selectedMap = "2018 Regional Final.fmp"
        self._player = None #needs to be implemented
        self._HUDController = None #needs to be implemented
        self._gameMode = self.GAME_MODE_SINGLE_PLAYER
        self._mapEditor = None
        self._serverIp = "localhost"
        self._networkClient = None
        self._notification = {"Text":""}
        self._viewMode = self.VIEW_MODE_MENU
        self._isFirstRun = True
        self.sceneHistory = []
        self.track = {"launchPads":[], "startFinishPlane":None,"countdownTime":3,"checkpoints":[],"nextCheckpoint":0,"lastCheckpoint":0}

        self._droneSettings = DroneSettings(self)
        self._radioSettings = RadioSettings(self)
        self._graphicsSettings = GraphicsSettings(self)

    #eventually we should implement propper logging
    def debug(self,output):
        output = str(output)
        if(self.LOG_LEVEL<=self.LOG_LEVEL_DEBUG):
            print("DEBUG: "+output)

    def log(self,output):
        output = str(output) #let's make sure that output is actually a string
        if(self.LOG_LEVEL<=self.LOG_LEVEL_INFO):
            print("LOG: "+output) #let's print it to the console
        with open(self.__logFile, 'a+') as saveFile: #let's write it to the log file
            saveFile.write(str(output)+"\n")
            saveFile.close()

    def error(self,output):
        output = str(output)
        if(self.LOG_LEVEL<=self.LOG_LEVEL_ERROR):
            print("ERROR: "+output)
        with open(self.__logFile, 'a+') as saveFile:
            saveFile.write(str(output)+"\n")
            saveFile.close()

    def loadSaveSettings(self):
        saveDict = logic.globalDict
        #first let's determin if this is the first time the game is being booted
        self._isFirstRun = (logic.globalDict == {})
        if(self._isFirstRun): #let's handle the first boot
            self.log("FlowState.loadSaveSettings: this is our first boot")

            droneSettings = {}
            radioSettings = {}
            graphicsSettings = {}

        else: #let's handle a returning user
            self.log("FlowState.loadSaveSettings: this isn't our first boot")

            #Let's load graphics settings
            profileIndex = 0#saveDict['currentProfile'] #let's get the index of the last user we were using
            profiles = saveDict['profiles'] #
            profile = profiles[profileIndex]

            #let's get the various settings for the profile
            droneSettings = profile['droneSettings']
            radioSettings = profile['radioSettings']
            graphicsSettings = profile['graphicsSettings']

        #read in the graphics settings
        self._graphicsSettings = GraphicsSettings(self, **graphicsSettings)

        #read in the drone settings
        self._droneSettings = DroneSettings(self, **droneSettings)

        #read in the radio settings
        self._radioSettings = RadioSettings(self, **radioSettings)

        if(self._isFirstRun): #if this is our first run, create a save file
            self.saveSettings()

    def saveSettings(self):

        #let's serialized versions of each of our settings
        serializedDroneSettings = self._droneSettings.getSerializedSettings()
        serializedRadioSettings = self._radioSettings.getSerializedSettings()
        serializedGraphicsSettings = self._graphicsSettings.getSerializedSettings()

        #let's define the structure for our save data
        saveData = {}
        saveData['version'] = self._version
        saveData['currentProfile'] = 0
        saveData['profiles'] = [{"droneSettings":serializedDroneSettings,"radioSettings":serializedRadioSettings,"graphicsSettings":serializedGraphicsSettings}]
        logic.globalDict = saveData
        logic.saveGlobalDict() #save the file to the disk

    def setEasyDefaults(self):
        #change the settings to something more appropriate for newbs
        self._droneSettings.setEasyDefaults()
        self._radioSettings.setEasyDefaults()

    def resetGameState(self):
        self.__init__()

    def getTimeLimit(self):
        return self._timeLimit

    def setTimeLimit(self,timeLimit):
        self._timeLimit = timeLimit

    def getCheckpoints(self):
        return self._checkpoints

    def setCheckpoints(self,checkpoints):
        self._checkpoints = checkpoints

    def getSelectedMap(self):
        return self._selectedMap

    def setSelectedMap(self,selectedMap):
        self._selectedMap = selectedMap

    def getPlayer(self):
        return self._player

    def setPlayer(self,player):
        self._player = player

    def getHUDController(self):
        return self._HUDController

    def setHUDController(self,HUDController):
        self._HUDController = HUDController

    def getGameMode(self):
        return self._gameMode

    def setGameMode(self,gameMode):
        self._gameMode = gameMode

    def getMapEditor(self):
        return self._mapEditor

    def setMapEditor(self,mapEditor):
        self._mapEditor = mapEditor

    def getServerIp(self):
        return self._serverIp

    def setServerIp(self,serverIp):
        self._serverIp = serverIp

    def getNetworkClient(self):
        return self._networkClient

    def setNetworkClient(self,networkClient):
        self._networkClient = networkClient

    def getNotification(self):
        return self._notification

    def setNotification(self,notification):
        self._notification = notification

    def getViewMode(self):
        return self._viewMode

    def setViewMode(self,viewMode):
        self._viewMode = viewMode

    def isFirstRun(self):
        return self._isFirstRun

    def getDroneSettings(self):
        return self._droneSettings

    def getRadioSettings(self):
        return self._radioSettings

    def getGraphicsSettings(self):
        return self._radioSettings
