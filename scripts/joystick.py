import bge.logic as logic
import math
import random
import copy
import bge.render as render
import time
import statistics
import FSNClient
import FSNObjects
utils = logic.utils
cont = logic.getCurrentController()
own = cont.owner
g = {}
profileIndex = logic.globalDict['currentProfile']
droneSettings = logic.globalDict['profiles'][profileIndex]['droneSettings']
radioSettings = logic.globalDict['profiles'][profileIndex]['radioSettings']
g = {**droneSettings, **radioSettings} #merge the two dictionaries
scene = logic.getCurrentScene()
mass = own.mass
gravity = 98*mass
camera = scene.objects['cameraMain']
game = scene.objects['Game']

try:
    logic.lastLogicTic
except:
    logic.lastLogicTic = float(time.perf_counter())
    print("creating time")
frameTime = float(time.perf_counter())-logic.lastLogicTic
logic.lastLogicTic = float(time.perf_counter())

if(logic.getAverageFrameRate()!=0):
    dm = frameTime*60
else:
    dm = 1
if(dm>1):
    dm = 1
def getAngularAcceleration():
    av = own.getAngularVelocity(True)

    if "init" in own:
        lastAv = own['lastAngularVel']
        own['angularAcc'] = getArrayProduct([av[0]-lastAv[0],av[1]-lastAv[1],av[2]-lastAv[2]])
        own['lastAngularVel'] = own.getAngularVelocity(True)

def respawn():
    if(utils.getMode()!=utils.MODE_MULTIPLAYER):
        launchPadNo = 0
    else:
        pass
    launchPadNo = random.randint(0,len(logic.utils.gameState['launchPads'])-1)
    launchPos = copy.deepcopy(logic.utils.gameState['launchPads'][launchPadNo].position)
    own['launchPosition'] = [launchPos[0],launchPos[1],launchPos[2]+1]
    own.position = own['launchPosition']
    print(logic.utils.gameState['launchPads'])
    print("SPAWNING!!!"+str(launchPadNo)+", "+str(launchPos))

def initAllThings():
    logic.player = own
    logic.player['camera'] = scene.objects['cameraMain']
    logic.utils.gameState['track']['nextCheckpoint'] = logic.defaultGameState['track']['nextCheckpoint']

    #logic.setPhysicsTicRate(120)
    #logic.setLogicTicRate(120)
    #print("max logic ticks per frame: "+str(logic.getMaxLogicFrame()))
    #print("logic ticks per second: "+str(logic.getLogicTicRate()))
    #print("max physics ticks per frame: "+str(logic.getMaxPhysicsFrame()))
    #logic.setLogicTicRate(60)

    print("physics ticks per second: "+str(logic.getPhysicsTicRate()))
    logic.ghosts = []
    av = own.getAngularVelocity(True)
    own['airSpeedDiff'] = 0
    own['lastAirSpeedDiff'] = 0
    own['lastAngularVel'] = av
    own['angularAcc'] = 0
    own['settled'] = False
    own['settleStartTime'] = time.perf_counter()
    print("SETTLE TIME IS "+str(own['settleStartTime']))
    own['settleDuration'] = 0
    own['settleFrameRates'] = []
    respawn()
    own['rxPosition'] = copy.deepcopy(logic.utils.gameState['launchPads'][0].position)
    own['rxPosition'][2]+=100
    own.orientation = logic.utils.gameState['launchPads'][0].orientation
    own['oporational'] = True
    own['vtxOporational'] = True
    own['damage'] = 0
    own.mass = g['weight']/1000
    logic.countingDown = True
    logic.countdown = -1
    logic.maxGForce = 0
    logic.finishedLastLap = False
    logic.utils.gameState['notification']['Text'] = ""
    #own['rxPosition'] = [-2279.73,-30.8,90]
    del game['shaderInit']

    print("init")
def getArrayProduct(array):
    a = array[0]
    b = array[1]
    c = array[2]
    return math.sqrt((a**2)+(b**2)+(c**2))

def getAcc():
    lv = own.getLinearVelocity(True)
    try:
        own['acc'] = (abs(own['lastVel']-getArrayProduct(lv)))
        try:
            if own['settled']:
                elapsedTime = 1/logic.getAverageFrameRate()
                force = ((abs(own['lastVel']-getArrayProduct(lv))/elapsedTime)/100)+1
                #print("force: "+str(force)+"\nelapsedTimie: "+str(elapsedTime))
                if own['armed']:
                    if logic.maxGForce < force:
                        logic.maxGForce = force
                        print(str(logic.maxGForce)+"G")
                else:
                    logic.maxGForce = 0
                logic.gForce = force
        except Exception as e:
            print(e)
            own['armed'] = False
            logic.gForce = 0
            logic.maxGForce = 0

        own['airSpeedDiff'] = (own['lastAirSpeedDiff']-lv[2])*0.01
        own['lastVel'] = getArrayProduct(lv)
    except Exception as e:
        try:
            own['lastVel'] = getArrayProduct(lv)
            own['acc'] = abs(own['lastVel']-getArrayProduct(lv))
            own['lastAirSpeedDiff'] = lv[2]
        except Exception as e:
            print(e)

def getStickPercentage(min,max,value):
    resolution = abs(min)+abs(max)
    percent = abs(((value-min)/resolution))
    (0+(100/2))/100.0
    return percent

def setup(camera,angle):
    if 'setup' not in own:
        initAllThings()
        angle = (angle/180)*math.pi
        camera.applyRotation([angle,0,0],True)
        own['setup'] = True
        own['canReset'] = False


def getSwitchValue(switchPercent,switchSetpoint,inverted):
    #if(switchInverted):
    #    switch = switchPercent>switchSetpoint
    #else:
    #    switch = switchPercent<switchSetpoint
    if(not inverted):
        switch = switchPercent>switchSetpoint
    else:
        switch = (1-switchPercent)>switchSetpoint
    return switch
def resetGame():
    #act = own.actuators["restart"]
    #act.useRestart = True
    #cont.activate(act)
    #own.position = logic.utils.gameState['spawnPoints'][0]#own['startPosition']
    #print("SPAWNING!!!"+str(logic.utils.gameState['spawnPoints'][0]))
    #own.orientation = own['startOrientation']
    scene.active_camera = camera
    own.setLinearVelocity([0,0,0],True)
    own.setAngularVelocity([0,0,0],True)

    own['lastAv'] = [0,0,0]
    if 'lastVel' in own:
        own['lastVel'] = [0,0,0]
    lapTimer = logic.utils.gameState['startFinishPlane']
    lapTimer['lap'] = -1
    lapTimer['race time'] = 0.0
    for ghost in logic.ghosts:
        ghost['obj']['fpvCamera'].endObject()
        ghost['obj']['spectatorCamera'].endObject()
        ghost['obj'].endObject()
    logic.ghosts = []
    own['canReset'] = False
    initAllThings()
    logic.utils.gameState['track']['nextCheckpoint'] = 0

def getRXVector(scale,rxPos):
    vectTo = own.getVectTo(rxPos)
    v = vectTo[1]
    vs = abs(v[0])+abs(v[1])+abs(v[2])
    vect = [(v[0]/vs)*scale,(v[1]/vs)*scale,(v[2]/vs)*scale]
    return vect

def applyVideoStatic():

    hitList = []

    lastHitPos = own.position
    for interference in range(1,100):
        hit = scene.active_camera.rayCast(own['rxPosition'], lastHitPos, 0.0, "", 0, 0, 0)
        hitPos = hit[1]
        if(hitPos == None):
            hitList.append(own['rxPosition'])
            break
        else:
            if(own.getDistanceTo(hitPos)<2):
                hitList.append(own['rxPosition'])
                break
            vScale = 2
            rxVect = getRXVector(vScale,own['rxPosition'])
            hitPos = [hitPos[0]+rxVect[0],hitPos[1]+rxVect[1],hitPos[2]+rxVect[2]]
            hitList.append(hitPos)
        lastHitPos = hitPos
    interference *= .1
    groundBreakup = (12-own.position[2])*0.3
    if(groundBreakup<1):
      groundBreakup = 1
    if(interference<1):
      interference = 1

    game['rfNoise'] = scene.active_camera.getDistanceTo(own['rxPosition'])*.01*groundBreakup*interference+game['eNoise']

def killVideo():
    pass
    #game['rfNoise'] = 100

def stickInputToDPS(rcData, superRate=70, rcRate=90, rcExpo=0.0, superExpoActive=True):
    #0.27
    inputValue = rcCommand(rcData, rcRate, rcExpo)
    angleRate = None
    if (superExpoActive):
        rcFactor = abs(inputValue) / (500 * rcRate / 100)
        rcFactor = 1 / (1 - rcFactor * superRate / 100)
        angleRate = rcFactor * 27 * inputValue / 16
    else:
        angleRate = (superRate + 27) * inputValue / 16
    #angleRate = constrain(angleRate, -8190, 8190); // Rate limit protection
    return angleRate/230

def rcCommand(rcData, rcRate, rcExpo):
    midRc = 1500
    tmp = min(abs(rcData - midRc), 500) / 100
    #tmp = abs(rcData)/100
    result = ((2500 + rcExpo * (tmp * tmp - 25)) * tmp * rcRate / 2500)
    if (rcData < midRc):
        result = -result
    return result



def main():
    #print("perf: "+str(1.0/frameTime))
    #print("afps: "+str(logic.getAverageFrameRate()))

    #Do the things and the stuff
    setup(camera,g['cameraTilt'])
    joy = cont.sensors["Joystick"]
    propRay = cont.sensors["Ray"]
    axis = joy.axisValues
    #print(axis)
    #xbox controllers....
    if(g['dedicatedThrottleStick'] == False):
        axis[g['throttleChannel']] -= (g['maxThrottle']-g['minThrottle'])/2
    if(axis != []): #if a radio is connected

        #stick offsets
        own['channel0'] = axis[0]
        own['channel1'] = axis[1]
        own['channel2'] = axis[2]
        own['channel3'] = axis[3]
        axis[g['rollChannel']]+=g['rollOffset']
        axis[g['yawChannel']]+=g['yawOffset']
        axis[g['pitchChannel']]+=g['pitchOffset']

        values = []
        center = 7000
        sensativity = .0008
        for value in axis:
            values.append((value-center)*sensativity)


        throttleInverted = -(int(g['throttleInverted'])-0.5)*2
        yawInverted = -(int(g['yawInverted'])-0.5)*2
        pitchInverted = -(int(g['pitchInverted'])-0.5)*2
        rollnverted = -(int(g['rollInverted'])-0.5)*2
        armInverted = -(int(g['armInverted'])-0.5)*2
        resetInverted = -(int(g['resetInverted'])-0.5)*2

        throttle = (axis[g['throttleChannel']-1])*throttleInverted
        yaw = axis[g['yawChannel']-1]*yawInverted
        pitch = axis[g['pitchChannel']-1]*pitchInverted
        roll = axis[g['rollChannel']-1]*rollnverted
        armSwitch = axis[g['armChannel']-1]*armInverted
        resetSwitch = axis[g['resetChannel']-1]*resetInverted

        throttlePercent = (getStickPercentage(g['minThrottle'],g['maxThrottle'],throttle))
        yawPercent = getStickPercentage(g['minYaw'],g['maxYaw'],yaw)
        pitchPercent = getStickPercentage(g['minPitch'],g['maxPitch'],pitch)
        rollPercent = getStickPercentage(g['minRoll'],g['maxRoll'],roll)
        armPercent = getStickPercentage(g['minArm'],g['maxArm'],armSwitch)
        resetPercent = getStickPercentage(g['minReset'],g['maxReset'],resetSwitch)
        armed = getSwitchValue(armPercent,g['armSetpoint'],g['armInverted'])
        reset = getSwitchValue(resetPercent,g['resetSetpoint'],g['resetInverted'])
        logic.throttlePercent = throttlePercent

    else: #if no radio is connected
        throttlePercent = 0
        yawPercent = 0
        pitchPercent = 0
        rollPercent = 0
        armed = False
        reset = False

    own['armed'] = armed
    rotationActuator = cont.actuators["movement"]

    #apply rotational force
    PE = g['pitchExpo']
    RE = g['rollExpo']
    YE = g['yawExpo']
    pp = (pitchPercent-.5)*2
    rp = (rollPercent-.5)*2
    yp = (yawPercent-.5)*2
    logic.errorLog = str(axis)
    ps = 1
    rs = 1
    ys = 1
    if(pp<0):
        ps = -1
    if(rp<0):
        rs = -1
    if(yp<0):
        ys = -1

    dps = 0.0174533
    RE = 1
    EXPO = 0
    #pitchForce = -(((abs(pp)*g['pitchRate']*85)**(RE))*ps)/foo
    #roleForce = (((abs(rp)*g['rollRate']*85)**(RE))*rs)/foo
    #yawForce = -(((abs(yp)*g['yawRate']*85)**(RE))*ys)/foo

    #-(abs(pp)*ps*dps*(g['pitchRate']*200))**((1+RE)*.82515)
    #print(abs(rp))
    #print((abs(rp)*rs*dps*(g['roleRate']*200)))
    #ps*pow((abs(pp)*(g['pitchRate']*200)),abs(pp)+2.2)*.434588)
    a = .48
    b = .834
    #pitchForce = -ps*pow((abs(pp)*(g['pitchRate']*200)),(abs(pp)*(PE)*a)+b)*dps
    #roleForce = rs*pow((abs(rp)*(g['rollRate']*200)),(abs(rp)*(RE)*a)+b)*dps
    #yawForce = -ys*pow((abs(yp)*(g['yawRate']*200)),(abs(yp)*(YE)*a)+b)*dps

    pitchForce = -stickInputToDPS((pitchPercent*1000)+1000,g['pitchSuperRate'],g['pitchRate'],g['pitchExpo'],True)
    roleForce = stickInputToDPS((rollPercent*1000)+1000,g['rollSuperRate'],g['rollRate'],g['rollExpo'],True)
    yawForce = -stickInputToDPS((yawPercent*1000)+1000,g['yawSuperRate'],g['yawRate'],g['yawExpo'],True)
    getAngularAcceleration()
    getAcc()
    if (own['oporational'] == True)&armed:
        if own['settled']:
            if(utils.getMode()!=utils.MODE_MULTIPLAYER):
                #WAYS YOU CAN KILL YOUR QUAD
                if(cont.sensors['PropStrike'].positive):

                    #print("PROP STRIKE!")
                    own['damage'] += own['acc']*0.1*throttlePercent
                    #print(own['damage'])
                if (own['acc'] > 65*2):
                    own['oporational'] = False
                    own['vtxOporational'] = False
                    #pass
                    print("Linear acceleration limit reached")
                if (abs(own['angularAcc']) > 50):
                    own['oporational'] = False
                    own['vtxOporational'] = False
                    #pass
                    print("Rotational acceleration limit reached")
                if (own['acc'] > 35):
                    if(own['propContact']):
                        own['damage'] += own['acc']*0.005
                if (abs(own['angularAcc']) > 25):
                    if(own['propContact']):
                        own['damage'] += own['angularAcc']*0.01
                if (own['damage'] > 2.5):
                    own['oporational'] = False
                    #pass
    lv = own.getLinearVelocity(True)
    if(own['oporational']):
        applyVideoStatic()
        if(armed):
            try:
                if own['airSpeedDiff'] < 0:
                    own['airSpeedDiff'] = 0
                propwash = math.pow((((own['airSpeedDiff']*.3)+(((own['damage']-0.1)*.5))*2)*.1145),1.5)*((throttlePercent*10)+.4)
                if propwash > 0.08:
                  propwash = 0.08

            except:
                propwash = 0




            #print(thrust)
            lvl = own.localLinearVelocity

            av = own.getAngularVelocity(True)

            #if(propRay.positive==False):
            if(not own['propContact']):
                rx = (random.randrange(0,200)-100)/300
                ry = (random.randrange(0,200)-100)/300
                rz = (random.randrange(0,200)-100)/300
                pwrx = (rx*propwash/(1+propwash*1.00005))*28
                pwry = (ry*propwash/(1+propwash*1.00005))*28
                pwrz = (rz*propwash/(1+propwash*1.00005))*28

                angularAcc = own['angularAcc']

                #AIR DAMPENING
                #FD = .99978 #use for X
                #FD = .99996 #use for true Z
                tdm = .9 #totalDragMultiplier
                sdm = 0.92 #sideDragMultiplier
                fdm = 0.9 #frontalDragMultiplier
                tdm = 1.3 #topDragMultiplier

                tdm = 0.0 #totalDragMultiplier
                sdm = 1 #sideDragMultiplier
                fdm = 1 #frontalDragMultiplier
                tdm = 1 #topDragMultiplier

                qd = [0.013014*dm*tdm*sdm,0.0111121*dm*fdm*tdm,0.0071081*dm*tdm] #air drag
                qd = [tdm,tdm,tdm]
                #own.setLinearVelocity([lv[0]/(1+qd[0]),lv[1]/(1+qd[1]),lv[2]/(1+qd[2])],True)
                #own.setLinearVelocity([lv[0]/(1+qd[0]),lv[1]/(1+qd[1]),lv[2]],True)
                #print(dm)
                st = 0.95*dm #how quick can the motor/pid orient the quad
                lav = own.getAngularVelocity(True)
                xav = (((pitchForce)*st)+(lav[0]*(1-st)))+pwrx
                yav = ((roleForce)*st)+(lav[1]*(1-st))+pwry
                zav = yawForce+pwrz
                #maxAngularAcceleration = 6
                #maxAngularAccelerationYaw = 6
                #xavDiff = pitchForce-lav[0]
                #yavDiff = roleForce-lav[1]
                #zavDiff = yawForce-lav[2]
                #print(str(xavDiff)+":"+str(yavDiff))
                #if abs(xavDiff) > maxAngularAcceleration:
                #    sign = ((1 if xavDiff < 0 else 0)-.5)*2
                #    xav = ((pitchForce+pwrx)*(0.5*dm))+(lav[0]*(1-(0.5*dm)))
                #    #print("x "+str(xavDiff))
                #if abs(yavDiff) > maxAngularAcceleration:
                #    sign = ((1 if yavDiff < 0 else 0)-.5)*2
                #    yav = ((roleForce+pwry)*(0.5*dm))+(lav[1]*(1-(0.5*dm)))
                #    #print("y "+str(yavDiff))
                #if abs(zavDiff) > maxAngularAccelerationYaw:
                #    sign = ((1 if zavDiff < 0 else 0)-.5)*2
                #    zav = ((yawForce+pwrz)*(0.5*dm))+(lav[2]*(1-(0.5*dm)))
                #    #print("z "+str(zavDiff))
                own.setAngularVelocity([xav,yav,zav], True)
                if own.position[2] <0:
                    p = own.position
                    own.position = [p[0],p[1],0]
                    #if av [2] <0:
                        #own.setAngularVelocity([av[0],av[1],0],False)
                #thrust = thrust/((propwash*0.89)+1)
                #maxRPM = g['rpm']#29.7230769
                motorKV = g['motorKV']
                cellCount = g['batteryCellCount']
                cellVoltage = 4.2
                maxRPM = motorKV*cellCount*cellVoltage
                propAdvance = 5

                maxThrust = g['thrust']/10
                propLoad = (((lvl[0]*.8)+(lvl[1]*.8)+(lvl[2]*1.2))*1000)/maxRPM
                #propLoad = (lvl[2]*10000)/maxRPM
                propAgressiveness = 1.4
                propThrottleCurve = 1

                currentRPM = maxRPM*throttlePercent
                #propLoad = lvl[2]*currentRPM/maxRPM



                #thrust = ((throttlePercent**propThrottleCurve)*.85)*(maxThrust-((propLoad**propThrottleCurve)/((maxSpeed**propThrottleCurve)/maxThrust)))
                thrustSetpoint = throttlePercent#+(abs(yawPercent-.5)*.25)
                if(thrustSetpoint>1):
                    thrustSetpoint = 1

                staticThrust = ((thrustSetpoint**propThrottleCurve))*maxThrust#*1000)#-(currentSpeed/maxSpeed)

                staticThrust = (thrustSetpoint**propThrottleCurve)*g['thrust']

                thrust = (staticThrust/10)-(propLoad)-(propwash*100)
                #thrust = staticThrust-(propLoad)-(propwash*100)
                if(thrust<0):
                    thrust = 0
                try:
                    thrust = thrust.real
                except:
                    pass
                propPitch = 4.6
                propSize = 5
                newtonToKg = 0.101971621
                motorNumber = 4
                currentRPM = throttlePercent*maxRPM
                #thrust = 100*((4.392399*(10**-8))*currentRPM*((propSize**3.5)/math.sqrt(propPitch))*((4.23333*(10**-4))*currentRPM*propPitch-(currentSpeed/10)))*newtonToKg*motorNumber

                #if(thrust<0):
                #    thrust = 0
                if 'lastThrust' in own:
                    thrust = (thrust*st)+(own['lastThrust']*(1-st))
                own['lastThrust'] = thrust

                if(float(logic.raceTimer)!=0.0):

                    own.applyForce([0,0,thrust],True)
                    
            if(g['autoLevel']):
                
                #own.setAngularVelocity([0,0,0], True)
                own.angularVelocity[0] = 0
                own.angularVelocity[1] = 0
                x = pitchPercent-0.5
                y = rollPercent-0.5
                z = 1
                levelTotal = abs(x)+abs(y)+abs(z)
                x/=levelTotal
                y/=levelTotal
                z/=levelTotal
                setOrientation = [x,-y,z]
                print(setOrientation)
                #own.alignAxisToVect(setOrientation, 2, 0.94)
                own.orientation = [-x,y,own.orientation.to_euler().z]

    else:
        thrust = 0
    if(not own['vtxOporational']):
        killVideo()

    if(reset == False)&(own['canReset']==False):
        own['canReset'] = True
        print("canReset = True")
    if((reset)&own['canReset']):
        if(utils.getMode()!=utils.MODE_MULTIPLAYER):
            resetGame()
        else:
            resetEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_MESSAGE,utils.getNetworkClient().clientID,"reset")
            utils.getNetworkClient().sendEvent(resetEvent)
            print("sending reset message")
            own['canReset'] = False

    own['lastAv'] = own.getAngularVelocity(True)
    #if(logic.getAverageFrameRate()>60):
    #    logic.setTimeScale(1)
own.applyForce([0,0,-98*own.mass],False)
def settle():
    logic.setTimeScale(1)
    own['settled'] = True
    logic.isSettled = True
    utils.log("SETTLING!!!!!!!")
def isSettled():
    if not own['settled']:
        logic.setTimeScale(0.001)
        if(utils.getMode()!=utils.MODE_MULTIPLAYER):
            logic.isSettled = False
            fps = logic.getAverageFrameRate()
            avgFPSList = own['settleFrameRates']
            avgFPSList.append(fps)
            deviation = 100
            if(len(avgFPSList)>1):
                deviation = statistics.stdev(avgFPSList)
            if len(avgFPSList)>100:
                if deviation < 300:
                    settle()
            else:

                own.setLinearVelocity([0,0,0],True)
                own.position = own['launchPosition']
            if len(avgFPSList)>1000:
                del avgFPSList[0]
                settle()
                utils.log("WARNING!!!: FPS did not become stable after 2000 frames. Expect physics instability...")
                utils.log("standard deviation: "+str(deviation))
        else: #we are in multiplayer and should wait a fixed time
            if ((time.perf_counter()-own['settleStartTime'])>3):
                settle()
                utils.log("settling due to time expiration in multiplayer")
    else:
        if(logic.finishedLastLap):
            logic.setTimeScale(0.001)
            #own.setLinearVelocity([0,0,0],True)

if(own.sensors['clock'].positive):
    main()
isSettled()
if(own.sensors['Message'].positive):
    resetGame()
