import bge
import copy
import time
from collections import OrderedDict

raceband = [5658,5695,5732,5769,5806,5843,5880,5917]
((abs(5658-5917))/25)+1
if not hasattr(bge, "__component__"):
    render = bge.render
    logic = bge.logic
    flowState = logic.flowState

class VTX(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Power Output (mw)", 25),
        ("Pit Mode",False),
        ("Channel", raceband[1])
    ])

    def start(self, args):
        flowState.log("vtx: start("+str(args)+")")
        self.power = args['Power Output (mw)']
        self.pitMode = int(args['Pit Mode'] == True)
        self.channel = args['Channel']
        self.signalStrength = 0
        self.object['vtx'] = self
        flowState.addRFEmitter(self)

    def setChannel(self,channelNumber):
        if(channelNumber>7):
            channelNumber = 7
        if(channelNumber<0):
            channelNumber = 0
        self.channel = raceband[channelNumber]

    def setVTXPower(self,power):
        if(power>1000):
            power = 1000
        if(power<5):
            power = 5
        self.power = power

    def setVTXPitMode(self,pitMode):
        self.pitMode = int(pitMode == True)

    def update(self):
        pass
