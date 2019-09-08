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

    def oncollision(self, obj, point, normal, points):
        #print("Hit by", obj)
        if(obj==logic.utils.getPlayerObject()):
            self.collision = (obj, point, normal, points)
        #for point in points:
        #    print(point.localPointA)
        #    print(point.localPointB)
        #    print(point.worldPoint)
        #    print(point.normal)
        #    print(point.combinedFriction)
        #    print(point.combinedRestitution)
        #    print(point.appliedImpulse)

    def start(self, args):
        self.lastPlayerPos = None
        self.entrance = None
        self.object["checkpoint"] = True
        self.collision = None
        self.object.collisionCallbacks = [self.oncollision]
        #print(self.object.collisionCallbacks)
        #print("start "+str(self.object.name))

    def getEntryAngle(self, v1, v2, acute):
        angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        return angle

    def setCheckpointVisibilities(self):
        for checkpoint in logic.utils.gameState['track']['checkpoints']:

            if(checkpoint['metadata']['checkpoint order'] == logic.utils.gameState['track']['nextCheckpoint']):
                checkpoint.visible = True
                self.enableCollision(checkpoint)
            else:
                checkpoint.visible = False
                self.disableCollision(checkpoint)
            #print("setting checkpoint "+str(checkpoint['metadata']['checkpoint order'])+" to collision group "+str(checkpoint.collisionGroup))

    def disableCollision(self,obj):
        mask = 4
        obj.collisionGroup = mask

    def enableCollision(self,obj):
        mask = 2#bytearray(mask)
        obj.collisionGroup = mask

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
                    cm = 2
                    ray = utils.getPlayerObject().rayCast(objto=pb, objfrom=pa, dist=0, prop="checkpoint", face=False, xray=True, poly=0,mask=cm)
                    hitObject, hitPoint, hitNormal = ray
                    #colHitObject, colPoint, colNormal, colPoints = self.collision
                    #render.drawLine(pa,pb,[0,0,0,1])
                    self.object['checked'] = True
                    if(hitObject==self.object) or (self.collision!=None):
                        self.collision = None
                        o = self.object.getVectTo(self.entrance.position)[1]
                        #print(o)
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
                            print("CHECKPOINT! "+str(hitCheckpointNumber))
                        else:
                            print("angle ("+str(difAngle)+") exceeds 90 "+str(hitCheckpointNumber))
                            #print(difAngle)

            self.lastPlayerPos = copy.deepcopy(utils.getPlayerObject().position)
