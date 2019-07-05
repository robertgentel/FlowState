import bge
from collections import OrderedDict

if not hasattr(bge, "__component__"):
    import time
    import numpy as np
    import math as m
    import copy
    import aud
    render = bge.render
    logic = bge.logic


class Checkpoint(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("checkpoint number", 1)
    ])

    def start(self, args):
        self.lastPlayerPos = None
        self.entrance = None
        self.object["checkpoint"] = True
        print("start "+str(self.object.name))

    def getEntryAngle(self, v1, v2, acute):
        angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        return angle

    def setCheckpointVisibilities(self):
        for checkpoint in logic.utils.gameState['track']['checkpoints']:
            if(checkpoint['metadata']['checkpoint order'] == logic.utils.gameState['track']['nextCheckpoint']):
                checkpoint.visible = True
            else:
                checkpoint.visible = False

    def playSound(self):
        sound = aud.Factory.file(bge.logic.expandPath('//sounds/checkpoint.wav'))
        scene = bge.logic.getCurrentScene()

        sound_device = aud.device()
        sound_device.distance_model = aud.AUD_DISTANCE_MODEL_LINEAR
        sound_device.listener_location = self.object.worldPosition
        sound_device.listener_velocity = [0,0,0]

        sound_handle = sound_device.play(sound)
        sound_handle.relative = False
        sound_handle.location = self.object.worldPosition
        sound_handle.velocity = self.object.getLinearVelocity()
        sound_handle.distance_maximum = 100
        sound_handle.distance_reference = 1

    def getNormalVect(self, vect):
        max = 0
        for i in vect:
            if abs(i) > max:
                max = i
        normal = []
        for i in range(0,len(vect)):
            normal.append(vect[i]/max)
        return normal
    def update(self):
        utils = logic.utils
        self.entrance = self.object.children[0]
        nextCheckpoint = logic.utils.gameState['track']['nextCheckpoint']
        hitCheckpointNumber = self.object['metadata']['checkpoint order']
        if(utils.getMode()!=utils.MODE_EDITOR):
            if(nextCheckpoint==hitCheckpointNumber):
                if self.lastPlayerPos!=None:
                    pa = self.lastPlayerPos
                    pb = utils.getPlayerObject().position
                    ray = utils.getPlayerObject().rayCast(objto=pb, objfrom=pa, dist=0, prop="checkpoint", face=False, xray=True, poly=0)
                    hitObject, hitPoint, hitNormal = ray
                    #render.drawLine(pa,pb,[0,0,0,1])
                    self.object['checked'] = True
                    if(hitObject==self.object):
                        o = self.object.getVectTo(self.entrance.position)[1]
                        v = utils.getPlayerObject().getLinearVelocity(False)

                        difAngle = m.degrees(self.getEntryAngle(v,o,True))
                        if(difAngle>90):
                            if logic.utils.gameState['track']['lastCheckpoint']==hitCheckpointNumber:
                                logic.utils.gameState['track']['nextCheckpoint'] = 0
                            else:
                                logic.utils.gameState['track']['nextCheckpoint']+=1
                            self.setCheckpointVisibilities()
                            startTime = time.perf_counter()
                            self.playSound()
                            endTime = time.perf_counter()
                            print("CHECKPOINT! "+str(endTime-startTime))
                        else:
                            print("angle exceeds 90 "+str(difAngle))
                            print(difAngle)

            self.lastPlayerPos = copy.deepcopy(utils.getPlayerObject().position)
