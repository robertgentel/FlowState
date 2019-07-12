import bge
import traceback
import os
from os.path import isfile, join
import ast
import json
logic = bge.logic
utils = logic.utils
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI
textColor = [1,1,1,1]
blockColor = [0,0,1,0.75]
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
    unknownAsset = utils.ASSET_CONCRETE_BLOCK
    idMap = {357:utils.ASSET_CONE,279:utils.ASSET_MGP_GATE,286:utils.ASSET_MGP_GATE,88:utils.ASSET_CHECKPOINT}
    
    prefab = gate['prefab']
    vdPos = gate['trans']['pos']
    vdOri = gate['trans']['rot']
    vdScale = gate['trans']['scale']
    pos = [vdPos[0]/10,vdPos[2]/10,vdPos[1]/10]
    ori = [0,0,0]#[vdOri[0],vdOri[2],vdOri[1]]
    scale = [vdScale[0]/100,vdScale[1]/100,vdScale[2]/100]
    asset = {}
    if prefab in idMap:
        asset["n"] = idMap[prefab]
    else:
        asset["n"] = unknownAsset
    asset["p"] = pos
    asset["o"] = ori
    asset["s"] = scale
    return asset

def convertVDMap(path):
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
        
    saveMapToFile(newMap,"importedMap.fmp")

def mapSelectAction(key,mapPath):
    convertVDMap(mapPath)
    #scenes = logic.getSceneList()
    #currentScene = logic.getCurrentScene()
    #for scene in scenes:
    #    if(scene!=currentScene):
    #        scene.end()
    #render.showMouse(0)
    #utils.selectMap(mapName)
    #utils.setMode(utils.MODE_SINGLE_PLAYER)
    #currentScene.replace("Map Editor")
 
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
    mapButton = UI.UIButton(mapButtonText,mapButtonBlock,mapSelectAction,"map",path)
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
        