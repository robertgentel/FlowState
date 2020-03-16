import bge
import copy
import time
from collections import OrderedDict

raceband = [5658,5695,5732,5769,5806,5843,5880,5917]
#(abs(5917-5917))+1
if not hasattr(bge, "__component__"):
    render = bge.render
    logic = bge.logic
    flowState = logic.flowState

class VRX(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Frequency", raceband[1])
    ])

    def start(self, args):
        flowState.log("vrx: start("+str(args)+")")
        self.frequency = args['Channel']
        self.interference = 0.0 #how muc of what we received was from interfering emitters
        self.snr = 1 #the signal to noise ratio
        self.object['vrx'] = self
        flowState.addRFReceiver(self)

    def getFrequency(self):
        return self.frequency

    def setChannel(self,channelNumber):
        if(channelNumber>7):
            channelNumber = 7
        if(channelNumber<0):
            channelNumber = 0
        self.frequency = raceband[channelNumber]

    def getChannel(self):
        for channel in range(0,len(raceband)):
            frequency = raceband[channel]
            if(frequency==self.frequency):
                break
        #print("got channel "+str(channel))
        #print("we are on frequency "+str(frequency))
        return channel

    def update(self):
        pass
