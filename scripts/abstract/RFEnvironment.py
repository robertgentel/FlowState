import bge
logic = bge.logic
render = bge.render
#this class keeps track of all the emitters and recievers in our radio frequency environment
class RFEnvironment:
    def __init__(self,flowState):
        flowState.log("RFEnvironment.init()")
        self.emitters = []
        self.receivers = []
        self.currentRXIndex = 0
        self.flowState = flowState

    def addEmitter(self,emitter):
        self.flowState.log("RFEnvironment.addEmitter()")
        self.emitters.append(emitter)

    def removeEmitter(self,emitter):
        self.flowState.log("RFEnvironment.removeEmitter()")
        self.emitters = [value for value in self.emitters if value != emitter] #removes all matching occurances of the rf emitter

    def addReceiver(self,receiver):
        self.flowState.log("RFEnvironment.addReceiver()")
        self.receivers.append(receiver)

    def removeReceiver(self,receiver):
        self.flowState.log("RFEnvironment.removeReceiver()")
        self.receivers = [value for value in self.receivers if value != receiver] #removes all matching occurances of the rf receiver

    def update(self, noiseFloor):
        if(self.receivers!=[]):
            rx = self.receivers[self.currentRXIndex] #let's get the rx the user is viewing
            signalStrength = noiseFloor
            strongestEmitter = None
            strongestSignalStrength = 0
            interference = 0 #we will use this to find out how much of the received signal is intentional or interference
            for vtx in self.emitters:
                disonance = ((abs(vtx.channel-rx.channel)*2)+1) #let's get a number between 1 and ~11 to represent how far detuned our vrx is from our vtx
                distance = vtx.object.getDistanceTo(rx.object)+0.1 #let's get the distance between the vtx and the vrx (but don't let it be 0)
                pitModePower = (1-vtx.pitMode)
                signalStrength = (vtx.power*pitModePower)/((distance/1000)**2)/disonance #let's use the inverse square law to determine the signal strength, then device it by the disonance of the channels.
                print
                #print("signal strength:"+str(signalStrength)+", disonance: "+str(disonance)+", power: "+str(vtx.power)+", channel: "+str(vtx.channel)+", pit mode: "+str(vtx.pitMode))
                if(signalStrength>strongestSignalStrength):
                    #let's note the emitter with the strongest signal as well as the value of that siganl strength
                    strongestEmitter = vtx
                    strongestSignalStrength = signalStrength
                    vtx.signalStrength = signalStrength

                interference += signalStrength

            if(strongestEmitter!=None):
                interference -= strongestSignalStrength #we don't want to count the current image as interference
                rx.interference = interference
                if(interference<=0):
                    interference = 0.1
                snr = strongestSignalStrength/interference
                if snr <= 0: #don't let snr = 0
                    snr = 0.1
                rx.snr = snr
                self.setCamera(strongestEmitter.object)
                render.drawLine(rx.object.position,vtx.object.position,[1,1,1])
                #self.flowState.log("emitters: "+str(self.emitters))
            #else:
                #self.flowState.log("no RF emitters!!!")
    def getCurrentVRX(self):
        vrx = None
        if(self.receivers!=[]):
            vrx = self.receivers[self.currentRXIndex]
        return vrx

    def setCamera(self,newCamera):
        scene = logic.getCurrentScene()
        activeCamera = scene.active_camera
        if(activeCamera!=newCamera):
            self.flowState.debug("switching to camera "+str(newCamera))
            scene.active_camera = newCamera
