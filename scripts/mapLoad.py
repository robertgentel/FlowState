import bge
logic = bge.logic
utils = logic.utils
import ast
import os
import math
cont = logic.getCurrentController()
blendPath = logic.expandPath("//")
def readFile(fileName):
    fileName = blendPath+"maps"+os.sep+fileName
    logic.utils.log("loading map: "+fileName)
    saveDataString = ""
    with open(fileName) as data:
        for line in data:
            saveDataString+=str(line)
    logic.utils.log("map load complete...")
    return ast.literal_eval(saveDataString)

def main():
    if(utils.getMode()!=utils.MODE_MULTIPLAYER):
        selectedMap = logic.utils.gameState['selectedMap']
        mapData = readFile(selectedMap)
        spawnMapElements(mapData)
        
def spawnMapElements(mapData):
    scene = logic.getCurrentScene()
    utils.log("getting assets...")
    utils.log(len(mapData['assets']))
    try:
        owner = logic.getCurrentScene().objects['Game']
    except:
        owner = logic.getCurrentScene().objects['Game.001']
    #clear any dead checkpoints
    logic.utils.gameState['track']['checkpoints'] = []

    for asset in mapData['assets']:
        spawn = object
        owner.position = asset['p']
        #owner.orientation = asset['o']

        if('s' in asset):
            s = asset['s']
            if asset['n']=="asset checkpoint square":
                owner.localScale = [s[0],0.75,s[2]] #checkpoints should always be fixed depth
            else:
                owner.localScale = s
        o = asset['o']
        owner.orientation = [math.radians(o[0]),math.radians(o[1]),math.radians(o[2])]
        #cont.actuators['spawner']
        newObj = scene.addObject(asset['n'],owner,0)
        newObj['solid'] = True
        for child in newObj.childrenRecursive:
            if 'spawn' in child: #we don't want spawners adding junk when we edit them
                child.endObject()
        if('m' in asset):

            m = asset['m']
            newObj['metadata'] = m
        if('m' not in  asset):
            utils.addMetadata(newObj)
            asset['m'] = newObj['metadata']
        if(asset['m'] == {}):
            utils.addMetadata(newObj)
        if('id' not in asset['m']):
            utils.addMetadata(newObj)
        print("loading metadata: "+str(newObj['metadata']))
        if(asset['n'] == utils.ASSET_START_FINISH):
            logic.utils.gameState['startFinishPlane'] = newObj
            utils.log("added start finish gate")
        if('checkpoint order' in newObj['metadata']):
            #if utils.getMode()!=utils.MODE_EDITOR:


            logic.utils.gameState['track']['checkpoints'].append(newObj)
            if newObj['metadata']['checkpoint order'] > logic.utils.gameState['track']['lastCheckpoint']:
                logic.utils.gameState['track']['lastCheckpoint'] = newObj['metadata']['checkpoint order']

        if(asset['n'] == "asset launch pad"):
            newSpawnPoint = newObj
            if "spawnPoints" in logic.utils.gameState:
                logic.utils.gameState['launchPads'].append(newSpawnPoint)
            else:
                logic.utils.gameState['launchPads'] = [newSpawnPoint]
            #utils.log("setting spawn point "+str(logic.utils.gameState))

