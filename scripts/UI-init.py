import bge
import traceback
logic = bge.logic
render = bge.render
render.showMouse(1)
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
UI = bge.UI
textColor = [1,1,1,1]
blockColor = [0,0,0.05,0.75]
utils = logic.utils

def beginnerAction():
    logic.utils.setSkillLevel(0)
    proceedAction()
    
def proAction():
    logic.utils.setSkillLevel(1)
    proceedAction()
    
def proceedAction():
    currentScene = logic.getCurrentScene()
    currentScene.replace("Menu Background")

def quitGameAction():
    logic.endGame()



if(owner['init']!=True):
    owner['init'] = True
    window = UI.Window()

    inset = 0.2
    
    
    if(utils.gameState[utils.STATE_FIRST_RUN]):
        welcomeText = UI.TextElement(window,[50+inset,70], textColor, 0, "Welcome to the Flow State drone racing simulator!")
        welcomeText = UI.TextElement(window,[50+inset,60], textColor, 0, "Have you flown a racing drone before?")
        beginnerBlockElement = UI.BoxElement(window,[30,30],3,2.5, blockColor, 1)
        beginnerText = UI.TextElement(window,beginnerBlockElement.position, textColor, 0, "First time")
        beginnerButton = UI.UIButton(beginnerText,beginnerBlockElement,beginnerAction)
        
        beginnerBlockElement = UI.BoxElement(window,[70,30],3,2.5, blockColor, 1)
        beginnerText = UI.TextElement(window,beginnerBlockElement.position, textColor, 0, "I've done this before")
        beginnerButton = UI.UIButton(beginnerText,beginnerBlockElement,proAction)
    else:
        multiplayerGameText = UI.TextElement(window,[10+inset,10], textColor, 0, "Loading...")
        proceedAction()
else:
    UI.run(cont)
    try:
        UI.run(cont)
    except Exception as e:
        logic.utils.log(traceback.format_exc())
        owner['init'] = -1
