import bge.logic as logic
import math
import random
import os
cont = logic.getCurrentController()
own = cont.owner
errorLog = logic.getCurrentScene().objects['HUDError']
laps = logic.getCurrentScene().objects['HUDLapCount']
lastLap = logic.getCurrentScene().objects['HUDLastLap']
bestLap = logic.getCurrentScene().objects['HUDBestLap']
times = logic.getCurrentScene().objects['HUDLapTimes']
holeshot = logic.getCurrentScene().objects['HUDHoleshot']
countdown = logic.getCurrentScene().objects['HUDCountdown']
gForceCounter = logic.getCurrentScene().objects['HUDgForceCounter']
aspectRatioCropper = logic.getCurrentScene().objects['aspectRatioCropper']
logic.flowState.setNotification(logic.getCurrentScene().objects['HUDNotification'])
laps['Text'] = "LAPS: "+logic.currentLap
lastLap['Text'] = "LAST LAP: "+logic.lastLapTime
bestLap['Text'] = "BEST LAP: "+logic.bestLapTime
holeshot['Text'] = "HOLESHOT: "+str(logic.holeshotTime)
errorLog['Text'] = "Error: "+logic.errorLog
droneSettings = logic.flowState.getSettings()
aspectRatioIs43 = droneSettings.aspectRatioIs4x3())
if(aspectRatioIs43):
    aspectRatioCropper.visible = True
else:
    aspectRatioCropper.visible = False
try:
    gForceCounter['Text'] = str(round(logic.gForce, 1))+"G"
except:
    pass

laps['Text'] = "LAPS: "+logic.currentLap
lastLap['Text'] = "LAST LAP: "+logic.lastLapTime
bestLap['Text'] = "BEST LAP: "+logic.bestLapTime
errorLog['Text'] = "Error: "+logic.errorLog
countdownTime = logic.flowState.track['countdownTime']
try:
    if logic.countingDown:

        if logic.countdown < 0:
            own['countdown'] = 0
            logic.countdown = 0
        else:
            logic.countdown = own['countdown']
            countdown['Text'] = int((countdownTime+1)-own['countdown'])
            if(own['countdown'] > countdownTime):
                logic.countingDown = False
                countdown['Text'] = "GO"
            if(own['countdown'] < countdownTime):
                logic.lapTimer['race time'] = 0.0
                logic.raceTimer = 0
            if(own['countdown'] > (countdownTime)):
                logic.countingDown = False
    else:
        if(own['countdown'] > countdownTime+0.5):
            countdown['Text'] = ""
except:
    logic.countingDown = False

timesText = "TIME: "+str(logic.raceTimer)
for i in range(0,len(logic.lapTimes)):
    timesText+='\n'
    timesText+="LAP "+str(i+1)+": "+str(logic.lapTimes[i])

times['Text'] = timesText
