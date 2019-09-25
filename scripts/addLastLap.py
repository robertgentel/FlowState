import bge.logic as logic
cont = logic.getCurrentController()
own = cont.owner
if own['lap'] >= 0:
    if(logic.finishedLastLap==False):
        if own.sensors['lap changed'].positive:
            logic.lapTimes.append(str(format(own['current_lap'], '.2f')))
            if(logic.lapTimer['race time'] > 120):
                logic.finishedLastLap = True
                logic.utils.gameState['notification']['Text'] = "race complete"
                logic.utils.gameState['track']['nextCheckpoint'] = logic.defaultGameState['track']['nextCheckpoint']
                print("race is complete")
