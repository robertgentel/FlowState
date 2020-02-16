import bge
import traceback
import os
from os.path import isfile, join
import ast
import json
import mathutils
import math
logic = bge.logic
utils = logic.utils
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI
textColor = [1,1,1,1]
blockColor = [0,0,0.05,0.75]
mapButtons = []
render.showMouse(1)


if "window" not in owner:
    owner['window'] = UI.Window()

window = owner['window']

def saveMapToFile(map,fileName):
    fileName = blendPath+"maps"+os.sep+fileName
    logic.utils.log("saving map: "+fileName)
    print("saving map to: "+fileName)
    try:
        with open(fileName, 'w+') as saveFile:
            saveFile.write(str(map))
            saveFile.close()
    except Exception as e:
        logic.utils.log("map save error: "+str(e))
    logic.utils.log("map save complete: "+fileName)

def readJSONFile(filePath):

    saveDataString = ""
    with open(filePath) as data:
        for line in data:
            saveDataString+=str(line)
    logic.utils.log("loading map: "+filePath)
    json_file = open(filePath)
    json_str = json_file.read()
    logic.utils.log("map load complete...")
    json_data = json.loads(json_str)
    return json_data

def convertAsset(gate,assetID):
    unknownAsset = utils.ASSET_CONE
    asdf = utils.ASSET_TABLE
    #50=shipping container
    #52=shipping container
    #155=car
    #590=car
    #311=shipping container
    #274=street light
    #248=Tents
    #292=Tent top
    #561=shacks
    #249=goal posts
    #344=total unkown
    idMap = {275:utils.ASSET_MGP_HURDLE,247:utils.ASSET_CONCRETE_BLOCK,344:utils.ASSET_CONCRETE_BLOCK,326:utils.ASSET_MGP_FLAG,303:utils.ASSET_CONE,319:utils.ASSET_MGP_FLAG,249:utils.ASSET_MGP_POLE,590:utils.ASSET_CONCRETE_BLOCK,561:utils.ASSET_CONCRETE_BLOCK,399:utils.ASSET_CONCRETE_BLOCK,246:utils.ASSET_MGP_POLE,292:utils.ASSET_CONCRETE_BLOCK,248:utils.ASSET_MGP_POLE,394:utils.ASSET_CONCRETE_BLOCK,30:utils.ASSET_PINE_TREE_TALL,18:utils.ASSET_PINE_TREE_TALL,274:utils.ASSET_MGP_POLE,311:utils.ASSET_CONCRETE_BLOCK,261:utils.ASSET_PINE_TREE_TALL,260:utils.ASSET_PINE_TREE_TALL,401:utils.ASSET_CONCRETE_BLOCK,155:utils.ASSET_CONCRETE_BLOCK,48:utils.ASSET_CONCRETE_BLOCK,52:utils.ASSET_CONCRETE_BLOCK,20:utils.ASSET_PINE_TREE_TALL,70:utils.ASSET_PINE_TREE_TALL,50:utils.ASSET_CONCRETE_BLOCK,100:utils.ASSET_PINE_TREE_TALL,28:utils.ASSET_PINE_TREE_TALL,108:utils.ASSET_CHECKPOINT,151:utils.ASSET_MGP_GATE_HANGING_LARGE,282:utils.ASSET_MGP_GATE_HIGH_LARGE,279:utils.ASSET_CONCRETE_BLOCK,285:utils.ASSET_MGP_GATE_LARGE,357:utils.ASSET_CONE,279:utils.ASSET_MGP_GATE,286:utils.ASSET_MGP_GATE_HANGING_LARGE,88:utils.ASSET_CHECKPOINT}

    prefab = gate['prefab']
    vdPos = gate['trans']['pos']
    vdOri = gate['trans']['rot']
    vdScale = gate['trans']['scale']
    pos = [vdPos[0]/10,vdPos[2]/10,vdPos[1]/10]
    ori = list(mathutils.Quaternion((math.radians(vdOri[0]),math.radians(vdOri[1]), math.radians(vdOri[2]), math.radians(vdOri[3]))).to_euler())
    ori = [math.degrees(-ori[0]),math.degrees(-ori[2]),math.degrees(-ori[1])]
    scale = [vdScale[0]/100,vdScale[2]/100,vdScale[1]/100]
    asset = {}
    if prefab in idMap:
        asset["n"] = idMap[prefab]
    else:
        asset["n"] = unknownAsset
    asset["p"] = pos
    asset["o"] = ori
    #if prefab == 247:
    #    asset['s'] = [2,2,2]
    #else:
    asset["s"] = scale
    print(asset)
    return asset

def convertVDMap(path,name):
    newMap = {"assets":[]}
    importedMap = readJSONFile(path)
    assetID = 0
    for gate in importedMap['gates']:
        print(gate)
        asset = convertAsset(gate,assetID)
        newMap['assets'].append(asset)
        assetID+=1

    for gate in importedMap['barriers']:
        print(gate)
        asset = convertAsset(gate,assetID)
        newMap['assets'].append(asset)
        assetID+=1
    depth = 0

    #let's clamp the lowest point on the map to the ground
    for asset in newMap['assets']:
        if(asset['p'][2] < depth):
            depth = asset['p'][2]
            print("new depth "+str(depth))
    for asset in newMap['assets']:
        asset['p'][2] = asset['p'][2]-depth

    saveMapToFile(newMap,name)

def mapSelectAction(key,mapInfo):
    mapPath = mapInfo[0]
    mapName = mapInfo[1]
    convertVDMap(mapPath,mapName)
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    render.showMouse(0)
    utils.selectMap(mapName)
    utils.setGameMode(utils.GAME_MODE_SINGLE_PLAYER)
    utils.setViewMode(utils.VIEW_MODE_PLAY)
    currentScene.replace("Map Editor")
def multiplayerAction():
    pass

def settingsAction():
    bge.logic.sendMessage("cam2")
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings")

def backAction():
    currentScene = logic.getCurrentScene()
    sceneHistory = logic.globalDict['sceneHistory']
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)

def passAction():
    pass

def addMapButton(path,name,spacing):
    buttonIndex = len(mapButtons)
    height = 70-(buttonIndex*spacing)
    print(height)
    mapButtonBlock = UI.BoxElement(window,[50,height],5,0.5, blockColor, 1)
    mapButtonText = UI.TextElement(window,mapButtonBlock.position, textColor, 0,name)
    mapButton = UI.UIButton(mapButtonText,mapButtonBlock,mapSelectAction,"map",[path,name])
    mapButtons.append(mapButton)

    owner['window'].add("mapButtonBlock"+name,mapButtonBlock)
    owner['window'].add("mapButtonText"+name,mapButtonText)
    owner['window'].add("mapButton"+name,mapButton)


if(owner['init']!=True):
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    headerBox = UI.BoxElement(window,[50,95],11,1, blockColor, 1)
    headerText = UI.TextElement(window,headerBox.position, textColor, 0, "SELECT MAP")
    blendPath = logic.expandPath("//")
    mapsPath = blendPath+"maps"+os.sep+"import"+os.sep
    f = []
    maps = [f for f in os.listdir(mapsPath) if os.path.isfile(os.path.join(mapsPath, f))]
    maps.append("CREATE NEW")
    #maps = ["2018 Regional Final.fmp", "2018 Regional Qualifier.fmp", "custom.fmp"]
    spacing = 8

    for m in range(0,len(maps)-1):
        map = maps[m]
        addMapButton(mapsPath+map,map,spacing)

    itemNumber = len(mapButtons)
    mapListBox = UI.BoxElement(window,[50,50],5,((itemNumber)*spacing)/10, blockColor, 15)
    mapList = UI.UIList(mapListBox,mapButtons,1)

    #back button
    backBlockElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    backText = UI.TextElement(window,backBlockElement.position, textColor, 0, "BACK")
    backButton = UI.UIButton(backText,backBlockElement,backAction)

    owner['window'].add("backBlockElement",backBlockElement)
    owner['window'].add("backText",backText)
    owner['window'].add("backButton",backButton)
    owner['window'].add("headerBox",headerBox)
    owner['window'].add("headerText",headerText)
    owner['window'].add("mapList",mapList)

else:
    try:
        #UI.run(cont)
        UI.runWindow(window,cont)
    except Exception as e:
        utils.log(traceback.format_exc())
        owner['init'] = -1
