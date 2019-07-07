import bge.logic as logic
import time
import math
scene = logic.getCurrentScene()
owner = logic.getCurrentController().owner
#logic.globalDict["playerQuad"] = owner
utils = logic.utils
def main():
    startTime = time.perf_counter()
    if "lastGhostUpdate" not in owner:
        owner["lastGhostUpdate"] = time.perf_counter()
    if abs(time.perf_counter()-owner["lastGhostUpdate"]) > (1/60.0):
        owner["lastGhostUpdate"] = time.perf_counter()
        if(utils.getMode()!=utils.MODE_MULTIPLAYER):
            if("startFinishPlane" in logic.utils.gameState):
                startFinishPlane = logic.utils.gameState["startFinishPlane"]
                lap = startFinishPlane["lap"]

                if lap < 0:
                    logic.ghosts = []
                else:
                    
                    if len(logic.ghosts)-1<lap:
                        ghostObject = addGhostQuad()
                        ghostObject["lap"] = lap 
                        logic.ghosts.append(createGhostData(owner,ghostObject))
                        #print("recording new ghost")
                    currentGhost = logic.ghosts[len(logic.ghosts)-1]
                    #if(lap<6):
                    recordGhostData(owner,currentGhost)
                    if len(logic.ghosts)>1:
                        for i in range(0,len(logic.ghosts)-1):
                            lastGhost = logic.ghosts[i]
                            setGhostData(lastGhost)
                            if(lastGhost["obj"]["spectatorCamera"]["cameraName"] == "ghost0"):
                                lastGhost["obj"]["spectatorCamera"]["cameraName"] = "ghostSpectate"+str(lap)
                            if(lastGhost["obj"]["fpvCamera"]["cameraName"] == "ghost0"):
                                lastGhost["obj"]["fpvCamera"]["cameraName"] = "ghostFPV"+str(lap)
        endTime = time.perf_counter()
        #print("main("+str(endTime-startTime))
def createGhostData(obj,ghostObject):
    startTime = time.perf_counter()
    digits = 3
    xa=round(obj.orientation[0][0],digits)
    xb=round(obj.orientation[0][1],digits)
    xc=round(obj.orientation[0][2],digits)
    ya=round(obj.orientation[1][0],digits)
    yb=round(obj.orientation[1][1],digits)
    yc=round(obj.orientation[1][2],digits)
    za=round(obj.orientation[2][0],digits)
    zb=round(obj.orientation[2][1],digits)
    zc=round(obj.orientation[2][2],digits)
    px = round(obj.position[0],digits)
    py = round(obj.position[1],digits)
    pz = round(obj.position[2],digits)
    result = {"obj":ghostObject,"currentFrame":0,"frames":[{"pos":[px,py,pz],"ori":[[xa,xb,xc],[ya,yb,yc],[za,zb,zc]]}]}
    endTime = time.perf_counter()
    #print("createGhostData("+str(endTime-startTime))
    return result

def recordGhostData(obj, currentGhost):
    if(not logic.finishedLastLap):
        startTime = time.perf_counter()
        digits = 3
        xa=round(obj.orientation[0][0],digits)
        xb=round(obj.orientation[0][1],digits)
        xc=round(obj.orientation[0][2],digits)
        ya=round(obj.orientation[1][0],digits)
        yb=round(obj.orientation[1][1],digits)
        yc=round(obj.orientation[1][2],digits)
        za=round(obj.orientation[2][0],digits)
        zb=round(obj.orientation[2][1],digits)
        zc=round(obj.orientation[2][2],digits)
        px = round(obj.position[0],digits)
        py = round(obj.position[1],digits)
        pz = round(obj.position[2],digits)
        currentGhost["frames"].append({"pos":[px,py,pz],"ori":[[xa,xb,xc],[ya,yb,yc],[za,zb,zc]]})
        endTime = time.perf_counter()
        #print("recordGhostData("+str(endTime-startTime))

def setGhostData(ghost):
    startTime = time.perf_counter()
    frame = ghost["currentFrame"]
    ghost["currentFrame"] += 1
    try:
        ghost["frames"][frame]
    except:
        ghost["currentFrame"] = -1
        frame = 0
    if(ghost["currentFrame"] < 180):
       disableGhostCollision(ghost["obj"])
    else:
        enableGhostCollision(ghost["obj"])
    ghost["obj"].position = ghost["frames"][frame]["pos"]
    ghost["obj"].orientation = ghost["frames"][frame]["ori"]
    #else:
    #    ghost["obj"]["camera"]
    #    #logic.sendMessage("disable shaders")
    #    #ghost["obj"].position = [0,0,-100000]
    endTime = time.perf_counter()
    #print("createGhostData("+str(endTime-startTime))
def addGhostQuad():
    
    actuator = owner.actuators["addGhost"]
    actuator.object = "ghostQuad"
    startTime = time.perf_counter()
    actuator.instantAddObject()
    endTime = time.perf_counter()
    #print("addGhostQuad("+str(endTime-startTime))
    obj = actuator.objectLastCreated
    disableGhostCollision(obj)
    obj.position = [0,0,-100000]
    
    return obj

def disableGhostCollision(obj):
    startTime = time.perf_counter()
    obj.collisionGroup = 4
    for child in obj.children:
        child.collisionGroup = 4
        for childOfChild in child.children:
            childOfChild.collisionGroup = 4
    endTime = time.perf_counter()
    #print("disableGhostCollision("+str(endTime-startTime))
        
def enableGhostCollision(obj):
    startTime = time.perf_counter()
    obj.collisionGroup = 1
    for child in obj.children:
        child.collisionGroup = 1  
        for childOfChild in child.children:
            childOfChild.collisionGroup = 1   
    endTime = time.perf_counter()
    #print("enableGhostCollision("+str(endTime-startTime))  

main()
