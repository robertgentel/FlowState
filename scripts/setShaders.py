import bge
render = bge.render
logic = bge.logic
owner = logic.getCurrentController().owner
utils = logic.utils
profileIndex = logic.globalDict['currentProfile']
profiles = logic.globalDict['profiles']
shaders = profiles[profileIndex]['graphicsSettings']['shaders']
if not "shaderInit" in owner:
    print("PLAYER FOUND!")
    if hasattr(logic,"player"):
        owner['shaderInit'] = True

        playerCamera = logic.player['camera']

        if shaders:
            playerCamera.lens= 5.823523998260498
            logic.sendMessage("enable shaders")
            print("enabling shaders")
        else:
            playerCamera.lens = 10
            logic.sendMessage("disable shaders")
            print("disabling shaders")