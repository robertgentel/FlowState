import bge
logic = bge.logic
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
owner = cont.owner
newCam = None
for object in scene.objects:
    if object != owner:
        if "cameraName" in object:
            print("object "+str(object.name)+" has property 'cameraName'")
            if object['cameraName'] == owner['cameraName']:
                print("name matches!")
                newCam = object
                break
if newCam != None:
    print(newCam)
    scene.active_camera = newCam
    if(newCam == "mainCamera"):
        logic.sendMessage("enable shaders")
    else:
        if "FPV" not in str(newCam['cameraName']):
            logic.sendMessage("disable shaders")
        else:
            logic.sendMessage("enable shaders")