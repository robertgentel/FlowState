import bge
import traceback
logic = bge.logic
render = bge.render
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI
textColor = [1,1,1,1]
blockColor = [0,0,0.05,0.75]
utils = logic.utils

profileIndex = logic.globalDict['currentProfile']
profiles = logic.globalDict['profiles']
profile = profiles[profileIndex]
graphicsSettings = profile['graphicsSettings']

def settingsAction(key,value):
    print(key,value)
    graphicsSettings[key] = value

def applySettings():
    #scenes = logic.getSceneList()
    #currentScene = logic.getCurrentScene()
    #for scene in scenes:
    #    if(scene!=currentScene):
    #        if(scene.name == "Main Game"):
    #             pass
    #            #currentMap = logic.utils.gameState["selectedMap"]
    #            #logic.utils.resetGameState()
    #            #logic.utils.gameState["selectedMap"] = currentMap
    #            #scene.restart()
    #
    logic.saveGlobalDict()
    logic.restartGame()
    #backAction()

def spawnBoolRow(label,height,key,action):

    rowBox = UI.BoxElement(window,[50,height],11,0.5, blockColor, 5)
    titleText = UI.TextElement(window,[rowBox.position[0]-30,rowBox.position[1]], textColor, 4, label)

    box = UI.BoxElement(window,[80,height],1,0.5, blockColor, 1)
    text = UI.TextElement(window,[box.position[0],box.position[1]], textColor, 0, "INVERTED")
    button = UI.UIButton(text,box,settingsAction)

    #indicatorText = UI.TextElement(window,[50,height], textColor, 0, "0")
    invertedBooleanButton = UI.UIBooleanInput(button,text,key,graphicsSettings[key])
    return invertedBooleanButton

def backAction():
    bge.logic.sendMessage("cam1")
    currentScene = logic.getCurrentScene()
    sceneHistory = logic.globalDict['sceneHistory']
    print(sceneHistory)
    backScene = sceneHistory[-2]
    removedScene = sceneHistory.pop(-1)
    removedScene = sceneHistory.pop(-1)
    print("removing scene "+str(removedScene))
    currentScene.replace(backScene)

if(owner['init']!=True):
    render.showMouse(1)
    logic.globalDict['sceneHistory'].append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    mainMenuBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "GRAPHIC")

    frameRate = spawnBoolRow("Frame Rate",20,"frameRate",settingsAction)
    shaders = spawnBoolRow("Filters",30,"shaders",settingsAction)
    specularity = spawnBoolRow("Specularity",40,"specularity",settingsAction)
    shadows = spawnBoolRow("Shadows",50,"shadows",settingsAction)
    shading = spawnBoolRow("Shading",60,"shading",settingsAction)
    raceLine = spawnBoolRow("Race Line",70,"raceLine",settingsAction)

    #back button
    backBlockElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    backText = UI.TextElement(window,backBlockElement.position, textColor, 0, "BACK")
    backButton = UI.UIButton(backText,backBlockElement,backAction)

    #apply button
    applyBox = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
    applyText = UI.TextElement(window,applyBox.position, textColor, 0, "APPLY")
    applyButton = UI.UIButton(applyText,applyBox,applySettings)

else:
    try:
        UI.run(cont)
    except Exception as e:
        utils.log(traceback.format_exc())
        owner['init'] = -1
