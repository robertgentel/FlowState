import bge
import traceback
import time
logic = bge.logic
render = bge.render

scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
flowState = logic.flowState
UI = bge.UI
flowState = logic.flowState
textColor = [1,1,1,1]
blockColor = flowState.menuButtonColor
textColorGrey = [0.5,0.5,0.5,1]

def restartAction():
    render.showMouse(0)
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    currentMap = logic.flowState.getSelectedMap()
    logic.flowState.resetGameState()
    logic.flowState.selectMap(currentMap)
    currentScene.replace("Main Game")

def mainMenuAction():
    if(logic.flowState.getGameMode()==logic.flowState.GAME_MODE_MULTIPLAYER):
        flowState.getNetworkClient().quit()
    else:
        scenes = logic.getSceneList()
        currentScene = logic.getCurrentScene()
        for scene in scenes:
            if(scene!=currentScene):
                scene.end()
        logic.flowState.resetGameState()
        logic.flowState.setViewMode(logic.flowState.VIEW_MODE_MENU)
        currentScene.replace("Menu Background")

def settingsAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("UI-settings")

def quitGameAction():
    logic.endGame()

def resumeAction():
    render.showMouse(0)
    currentScene = logic.getCurrentScene()
    currentScene.end()
    if(flowState.getGameMode()!=flowState.GAME_MODE_MULTIPLAYER):
        logic.getSceneList()[0].resume()

def doNothingAction():
    pass

if(owner['init']!=True):
    flowState.setViewMode(flowState.VIEW_MODE_MENU)

    #pause the main game if we aren't in multiplayer
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    print(scenes)
    if(flowState.getGameMode()!=flowState.GAME_MODE_MULTIPLAYER):
        scenes[0].suspend()

    flowState.sceneHistory.append(logic.getCurrentScene().name)
    owner['init'] = True
    window = UI.Window()

    inset = 0.2

    mainMenuBlock = UI.BoxElement(window,[50,95],11,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "PAUSE MENU")

    mainMenuBlock = UI.BoxElement(window,[10,50],2,1, blockColor, 1)
    mainMenuText = UI.TextElement(window,mainMenuBlock.position, textColor, 0, "MAIN MENU")
    mainMenuButton = UI.UIButton(mainMenuText,mainMenuBlock,mainMenuAction)

    doNothingAction

    if(flowState.getGameMode()!=flowState.GAME_MODE_MULTIPLAYER):
        restartBlock = UI.BoxElement(window,[50,50],2,1, blockColor, 1)
        restartText = UI.TextElement(window,restartBlock.position, textColor, 0, "RESTART")
        restartButton = UI.UIButton(restartText,restartBlock,restartAction)
    else:
        restartBlock = UI.BoxElement(window,[50,50],2,1, blockColor, 1)
        restartText = UI.TextElement(window,restartBlock.position, textColorGrey, 0, "RESTART")
        restartButton = UI.UIButton(restartText,restartBlock,doNothingAction)

    settingsBlockElement = UI.BoxElement(window,[90,50],2,1, blockColor, 1)
    settingsText = UI.TextElement(window,settingsBlockElement.position, textColor, 0, "SETTINGS")
    settingsButton = UI.UIButton(settingsText,settingsBlockElement,settingsAction)

    quitBlockElement = UI.BoxElement(window,[90,10],1,.5, blockColor, 1)
    quitText = UI.TextElement(window,quitBlockElement.position, textColor, 0, "QUIT")
    quitButton = UI.UIButton(quitText,quitBlockElement,quitGameAction)

    resumeElement = UI.BoxElement(window,[10,10],1,.5, blockColor, 1)
    resumeText = UI.TextElement(window,resumeElement.position, textColor, 0, "RESUME")
    resumeButton = UI.UIButton(resumeText,resumeElement,resumeAction)


else:
    try:
        UI.run(cont)
    except Exception as e:
        flowState.log(traceback.format_exc())
        owner['init'] = -1
