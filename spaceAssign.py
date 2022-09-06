import math
import os
import traci
from decimal import Decimal
from sympy import *
import threading
import time
sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c",
           "C:\\Users\\user\\Desktop\\sumo\\laneChange\\space\\myConfig.sumocfg"]

traci.start(sumoCmd)
step = 0
space = []
changeFlag = []
changeSpeedTime = []
stopChangeFlag = 0
allChangeFlag = -1
zoomOut = []
allAre1 = 0

x = Symbol('x')

# allSpace = []
fleetPosition = []
otherPosition = []

fleetLandID = []
otherLandID = []


# test area
changeFlag2 = []
changeSpeedTime2 = []
def changeInit2():
    for i in range(6):
        changeFlag2.append(0)

def changeTime2():
    for i in range(6):
        changeSpeedTime2.append(-1)

def calFollowSpeed(nowSpeed, frontSpeed, distance, notice, brakeMax):
    follow = (nowSpeed**2 * brakeMax) / (frontSpeed**2 +2 * brakeMax * (distance - nowSpeed * notice))
    return follow

def calRiskBySpeed(nowSpeed, frontSpeed, maxBrake, notice, expect):
    solve_value = solve([((nowSpeed**2 * maxBrake)/(frontSpeed**2 + 2*maxBrake*(x - nowSpeed * notice)) / maxBrake) - expect],[x])
    return solve_value

def calSlideDistace(speed, maxBrake, time):
    slideDistace = speed * time - 0.5 * maxBrake * (time**2)
    return slideDistace


# 0823
def initPosition():
    for i in range(11):
        fleetPosition.append(0)
        otherPosition.append(0)
        fleetLandID.append(-1)
        otherLandID.append(-1)

def getAllPosition():
    for i in range(11):
        veh = "veh" + str(i)
        no = "no" + str(i)
        fleetPosition[i] = traci.vehicle.getPosition(veh)[0]
        otherPosition[i] = traci.vehicle.getPosition(no)[0]
        # print (type(fleetPosition[i]))
        # print("fleet: "+str(traci.vehicle.getLaneIndex(veh)))

def getAllLaneID():
    for i in range(11):
        veh = "veh" + str(i)
        no = "no" + str(i)
        fleetLandID[i] = traci.vehicle.getLaneIndex(veh)
        otherLandID[i] = traci.vehicle.getLaneIndex(no)
        # print("veh"+str(i)+" LaneID: "+ str(fleetLandID[i]))

def calClosestCar(now, index):
    landID = traci.vehicle.getLaneIndex(now)
    nowPosition = traci.vehicle.getPosition(now)[0]
    # min = -1
    minIndex = 0
    fleetOrNot = -1

    # if changeFlag[index] == 1 :
    #     min = -1
    #     for i in range(11):
    #         if nowPosition < fleetPosition[i] and fleetPosition[i] - nowPosition > 1:
    #             if min == -1:
    #                 min = fleetPosition[i] - nowPosition
    #                 minIndex = i
    #                 fleetOrNot = 1
    #             else:
    #                 if min > fleetPosition[i] - nowPosition:
    #                     min = fleetPosition[i] - nowPosition
    #                     minIndex = i
    #                     fleetOrNot = 1
    #     for i in range(11):
    #         if nowPosition < otherPosition[i] and otherPosition[i] - nowPosition > 1:
    #             if min == -1:
    #                 min = otherPosition[i] - nowPosition
    #                 minIndex = i
    #                 fleetOrNot = 0
    #             else:
    #                 if min > otherPosition[i] - nowPosition:
    #                     min = otherPosition[i] - nowPosition
    #                     minIndex = i
    #                     fleetOrNot = 0
    #                     print("sfdsff")
    # else:
    # print("Nothing.............")
    min = -1
    for i in range(11):
        if landID == fleetLandID[i] and fleetPosition[index] < fleetPosition[i] and i != index:
            if min == -1:
                min = fleetPosition[i] - fleetPosition[index]
                minIndex = i
                fleetOrNot = 1
                # print("case 1: "+str(min))
            else:
                if min > fleetPosition[i] - fleetPosition[index]:
                    min = fleetPosition[i] - fleetPosition[index]
                    minIndex = i
                    fleetOrNot = 1
                    # print("case 2: "+str(min))
    for i in range(11):
        if landID == otherLandID[i] and fleetPosition[index] < otherPosition[i] and i != index:
            if min == -1:
                min = otherPosition[i] - fleetPosition[index]
                minIndex = i
                fleetOrNot = 0
                # print("case 3: "+str(min))
            else:
                if min > otherPosition[i] - fleetPosition[index]:
                    min = otherPosition[i] - fleetPosition[index]
                    minIndex = i
                    fleetOrNot = 0
                    # print("case 4: "+str(min))

    return [fleetOrNot, minIndex]
            
            
            


def calSpace():
    for i in range(11):
        vehString3 = "no"+str(i)
        vehString4 = "no"+str(i+1)
        tmpSpace = abs(traci.vehicle.getPosition(vehString3)[
                       0] - traci.vehicle.getPosition(vehString4)[0]) - traci.vehicle.getLength(vehString3)
        space.append(tmpSpace)
    print("space: "+str(space))


def noNoChange():

    traci.vehicle.setLaneChangeMode("no0", 0b000000000000)
    traci.vehicle.setLaneChangeMode("no1", 0b000000000000)
    traci.vehicle.setLaneChangeMode("no2", 0b000000000000)
    traci.vehicle.setLaneChangeMode("no3", 0b000000000000)

    traci.vehicle.setLaneChangeMode("no4", 0b000000000000)
    traci.vehicle.setLaneChangeMode("no5", 0b000000000000)
    traci.vehicle.setLaneChangeMode("no6", 0b000000000000)
    traci.vehicle.setLaneChangeMode("no7", 0b000000000000)

    traci.vehicle.setLaneChangeMode("no8", 0b000000000000)
    traci.vehicle.setLaneChangeMode("no9", 0b000000000000)
    traci.vehicle.setLaneChangeMode("no10", 0b000000000000)
    traci.vehicle.setLaneChangeMode("no11", 0b000000000000)


def speedModeInit():
    speedMode = 0
    traci.vehicle.setSpeedMode("veh0", speedMode)
    traci.vehicle.setSpeedMode("veh1", speedMode)
    traci.vehicle.setSpeedMode("veh2", speedMode)
    traci.vehicle.setSpeedMode("veh3", speedMode)

    traci.vehicle.setSpeedMode("veh4", speedMode)
    traci.vehicle.setSpeedMode("veh5", speedMode)
    traci.vehicle.setSpeedMode("veh6", speedMode)
    traci.vehicle.setSpeedMode("veh7", speedMode)

    traci.vehicle.setSpeedMode("veh8", speedMode)
    traci.vehicle.setSpeedMode("veh9", speedMode)
    traci.vehicle.setSpeedMode("veh10", speedMode)
    traci.vehicle.setSpeedMode("veh11", speedMode)


def changeCarSpeedMode(car, speedMode):
    traci.vehicle.setSpeedMode(car, speedMode)


def changeInit():
    for i in range(11):
        changeFlag.append(0)


def speedInit():
    for i in range(11):
        vehString3 = "veh"+str(i)
        # no = "no"+str(i)
        traci.vehicle.setSpeed(vehString3, 20)
        # traci.vehicle.setSpeed(no, 10)


def changeTime():
    for i in range(11):
        changeSpeedTime.append(-1)


def initZoomFlag():
    for i in range(10):
        zoomOut.append(-1)

def riskFollowing():
    global allAre1
    allAre1 = 0
    for i in range(1, 11):
        now = "veh"+str(i)
        front = "veh"+str(i-1)
        closeset = calClosestCar(now, i)
        if closeset[0] == 0:
            front = "no"+str(closeset[1])
        elif closeset[0] == 1:
            front = "veh"+str(closeset[1])
        # print(now+" follwing: "+front)
        
        if "no" in front:
            notice = 1.5
        elif "no" in now:
            notice = 1.5
        elif "veh" in now and  "veh" in front:
            notice = 0.1

        # notice = 0.1
        frontSpeed = traci.vehicle.getSpeed(front)
        nowSpeed = traci.vehicle.getSpeed(now)
        gap = traci.vehicle.getPosition(front)[0] - traci.vehicle.getPosition(now)[0] - 4
        acci = calFollowSpeed(nowSpeed, frontSpeed, gap, notice, 8)
        

        followRisk = acci / 8
        if abs(followRisk) >= 1:
            # solve_value = solve([((nowSpeed**2 * 8)/(frontSpeed**2 + 2*8*(x - nowSpeed * notice)) / 8) - 1],[x])
            solve_value = calRiskBySpeed(nowSpeed, frontSpeed, 8, notice, 1)
            # print("nowSpeed: "+str(nowSpeed)+" frontSpeed: "+str(frontSpeed)+" safetyDistace: "+ str(solve_value))
            if ":" in str(solve_value):
                characters = "{,x:}"
                tempString = str(solve_value)
                for j in range(len(characters)):
                    tempString = tempString.replace(characters[j], "")
                saftyDistace = float(tempString)

            # if i == 9:
            #     print("\n"+now+" follwing: "+front)
            #     print("nowSpeed: "+str(nowSpeed))
            #     print("frontSpeed: "+str(frontSpeed))
            #     print("notice: "+str(notice))
            #     print("laneID: "+str(fleetLandID[i]))
            #     print("followRisk : " +str(followRisk))
            #     print("safe distace : " +str(saftyDistace))
            #     print("gap : " +str(gap))
            #     print("acci: "+ str(acci))
            # 
              
            # if saftyDistace > gap:
            #     offset = saftyDistace - gap

            if saftyDistace > gap:
                oneSpeed = 8 / 10
                if traci.vehicle.getSpeed(now) - oneSpeed > 0:
                    newSpeed = traci.vehicle.getSpeed(now) - oneSpeed
                    traci.vehicle.setSpeed(now, newSpeed)
                    if i == 9:
                        print("oneSpeed : " +str(oneSpeed))
                        print("newSpeed : " +str(newSpeed))



            # if saftyDistace > gap:
            #     crashTime = gap / (nowSpeed)
            #     distaceOffset = saftyDistace - gap
            #     if crashTime <= notice:
            #         distaceOffset10 = (distaceOffset / 8) / 10
            #     else:
            #         oneSecondPlus = distaceOffset / crashTime
            #         distaceOffset10 = (distaceOffset / oneSecondPlus) / 10
            #     # print("distaceOffset10: "+str(distaceOffset10 * 10))
            #     if traci.vehicle.getSpeed(now) - distaceOffset10 > 0:
            #         newSpeed = traci.vehicle.getSpeed(now) - distaceOffset10
            #         traci.vehicle.setSpeed(now, newSpeed)
            #         # print ("newSpeed: "+str(newSpeed))
            # elif abs(saftyDistace - gap) <= 0.1:
            #     return 0
            # elif saftyDistace < gap:
            #     distaceOffset = gap - saftyDistace
            #     distaceOffset10 = (distaceOffset / 6) 
            #     newSpeed = traci.vehicle.getSpeed(now) + distaceOffset / 2
            #     traci.vehicle.setSpeed(now, newSpeed)
        else:
            allAre1 = allAre1 + 1
    return allAre1
            

# def backRiskSpeed():
#     while step < 40000:
#         if step > 1:
#             riskFollowing(0.1)

# t = threading.Thread(target = backRiskSpeed)

while step < 40000:
    traci.simulationStep()
    if step == 0:
        os.remove("output.txt")
        print("File removed successfully")
        path = 'output.txt'
        f = open(path, 'a')

        os.remove("output2.txt")
        print("File removed successfully")
        path = 'output2.txt'
        f2 = open(path, 'a')

        os.remove("output3.txt")
        print("File removed successfully")
        path = 'output3.txt'
        f3 = open(path, 'a')
        # t.start()

    # if step > 0 and step % 100 == 0:
    #    calSpace()

    if step == 0:
        initPosition()

        # solve_value = solve([((10**2 * 8)/(10**2 + 2*8*(x - 10 * 0.1)) / 8) - 1],[x])
        # calRiskBySpeed(30,30,8,0,1)
        # print(calRiskBySpeed(30,30,8,0,1))


        traci.vehicle.setEmergencyDecel("veh11", 0)
        traci.vehicle.setSpeed("veh11", 0)

        # traci.vehicle.setLaneChangeMode("veh0",0b001000000000)
        # traci.vehicle.setLaneChangeMode("veh1",0b001000000000)
        # traci.vehicle.setLaneChangeMode("veh2",0b001000000000)
        # traci.vehicle.setLaneChangeMode("veh3",0b001000000000)

        traci.vehicle.setLaneChangeMode("veh0", 0b000000000000)
        traci.vehicle.setLaneChangeMode("veh1", 0b000000000000)
        traci.vehicle.setLaneChangeMode("veh2", 0b000000000000)
        traci.vehicle.setLaneChangeMode("veh3", 0b000000000000)

        traci.vehicle.setLaneChangeMode("veh4", 0b000000000000)
        traci.vehicle.setLaneChangeMode("veh5", 0b000000000000)
        traci.vehicle.setLaneChangeMode("veh6", 0b000000000000)
        traci.vehicle.setLaneChangeMode("veh7", 0b000000000000)

        traci.vehicle.setLaneChangeMode("veh8", 0b000000000000)
        traci.vehicle.setLaneChangeMode("veh9", 0b000000000000)
        traci.vehicle.setLaneChangeMode("veh10", 0b000000000000)
        traci.vehicle.setLaneChangeMode("veh11", 0b000000000000)

        noNoChange()
        speedModeInit()
        speedInit()
        changeInit()
        changeTime()

# test area -----------------------------------
        changeInit2()
        changeTime2()

    veh0 = traci.vehicle.getPosition("veh0")
    veh11 = traci.vehicle.getPosition("veh11")

    if step > 0:
        getAllPosition()
        getAllLaneID()
        riskFollowing()

    # if step == 1000:
    #    # traci.vehicle.changeLane("veh1", 1, 300)
    #    for i in range(11):
    #       tmp = "no" + str(i)
    #       traci.vehicle.setSpeed(tmp, 0)

    # if step == 3000:
    #    for i in range(11):
    #       veh = "veh" + str(i)
    #       traci.vehicle.setSpeed(veh, 20)

    if step == 1:
        for i in range(10):
            vehString = "veh"+str(i+1)
            traci.vehicle.setSpeed(vehString, 30)

    # if step > 300:
    #     for i in range(10):
    #         front = "veh"+str(i)
    #         back = "veh" + str(i+1)
    #         if traci.vehicle.getPosition(front)[0]-traci.vehicle.getPosition(back)[0] < 20:
    #            traci.vehicle.setSpeed(back, 20)

    # if step > 1500 and stopChangeFlag < 11 and allAre1 > 9:
    if step > 1500 and stopChangeFlag < 11:
        for i in range(11):
            if i-1 >= 0:
                veh = "veh" + str(i)
                no = "no" + str(i)
                veh1 = "veh" + str(i-1)
                no1 = "no" + str(i+1)
                frontSpeed = traci.vehicle.getSpeed(no)
                nowSpeed = traci.vehicle.getSpeed(veh1)
                frontSlideDistace = calSlideDistace(frontSpeed, 8, 1.5)
                safetyDistace = 0
                if traci.vehicle.getPosition(no)[0]-traci.vehicle.getPosition(veh1)[0] - 4 < 60:
                    solve_value = calRiskBySpeed(frontSpeed, frontSpeed, 8, 1.5, 1)
                    if ":" in str(solve_value):
                        characters = "{,x:}"
                        tempString = str(solve_value)
                        for j in range(len(characters)):
                            tempString = tempString.replace(characters[j], "")
                        safetyDistace = float(tempString)
                gap = traci.vehicle.getPosition(no)[0]-traci.vehicle.getPosition(veh1)[0] - 4

                if i == 10:
                    print ("gap: " + str(gap))
                    print ("safetyDistace: " + str(safetyDistace))
                    print ("gap + frontSlideDistace: " + str(gap + frontSlideDistace))
                    print ("nowSpeed * 1.5: " + str(nowSpeed * 1.5))
                if gap > 0:
                #   if i > 0 and traci.vehicle.getPosition(no)[0]-traci.vehicle.getPosition(veh1)[0] < 40 and changeFlag[i] == 0:
                    if i > 0 and gap + frontSlideDistace > (frontSpeed * 1.5)  and  gap - safetyDistace < 1 and safetyDistace < gap  and changeFlag[i] == 0:
                        if i % 2 == 0:
                            traci.vehicle.changeLane(veh1, 1, 300)
                            traci.vehicle.changeLane(veh, 1, 300)
                            traci.vehicle.setSpeed(veh1, frontSpeed)
                            traci.vehicle.setSpeed(veh, frontSpeed)
                            changeFlag[i] = 1
                            changeSpeedTime[i] = step + 150
                            stopChangeFlag = stopChangeFlag + 1
                # traci.vehicle.setSpeed(veh, -1)

    # if step > 2000 and  allChangeFlag == -1:
    #    for i in range(11):
    #       if step == changeSpeedTime[i]:
    #          veh = "veh" + str(i)
    #          no = "no" + str(i)
    #          veh1 = "veh" + str(i-1)
    #          print("now changing"+ str(i))
    #          if i % 2 == 0:
    #             traci.vehicle.setSpeed(veh1, traci.vehicle.getSpeed(no))
    #             tempSpeed = traci.vehicle.getSpeed(no)
    #             changeCarSpeedMode(veh, 1)
    #             traci.vehicle.setSpeed(veh,  -1)
             
    #    if -1 in changeSpeedTime == False:
    #       allChangeFlag = 0



    # if step > 2000 and stopChangeFlag < 6:
    #     for i in range(6):
    #         veh = "veh" + str(2*i)
    #         no = "no" + str(2*i)
    #         vehBack = "veh" + str(2*i+1)
    #         if i % 2 == 0:
    #             if traci.vehicle.getPosition(no)[0]-traci.vehicle.getPosition(veh)[0] < 60 and changeFlag2[i] == 0:
    #                 traci.vehicle.changeLane(veh, 1, 300)
    #                 traci.vehicle.changeLane(vehBack, 1, 300)
    #                 changeSpeedTime2[i] = step + 200
    #                 stopChangeFlag = stopChangeFlag + 1

    # if step > 2000 and  allChangeFlag == -1:
    #     for i in range(6):
    #         if step == changeSpeedTime2[i]:
    #             veh = "veh" + str(2*i)
    #             no = "no" + str(2*i)
    #             vehBack = "veh" + str(2*i+1)
    #             print("now changing"+ str(i))
    #             if i % 2 == 0:
    #                 traci.vehicle.setSpeed(veh, traci.vehicle.getSpeed(no))
    #                 traci.vehicle.setSpeed(vehBack,  traci.vehicle.getSpeed(no))
             
    # if -1 in changeSpeedTime2 == False:
    #     allChangeFlag = 0
    

    # if traci.vehicle.getLaneID("veh0") == traci.vehicle.getLaneID("veh11") and abs(veh0[0] - veh11[0]) < 10:
    #    for i in range(11):
    #       vehString = "veh"+str(i)
    #       traci.vehicle.changeLane(vehString, 1, 1000.0)

    # if step == 7000:
    #    traci.vehicle.changeLane("veh11", 0,100)
    #    print("etsetst: "+str(step))

    if step > -1:
        save = ""
        for i in range(11):
            vehString = "veh"+str(i)
            save = save + " " + str(traci.vehicle.getSpeed(vehString))
        f.write(str(step/100)+save+"\n")
        save = ""
        for i in range(10):
            vehString = "veh"+str(i)
            vehString2 = "veh"+str(i+1)
            gap = 0
            gap = abs(traci.vehicle.getPosition(vehString2)[
                      0]-traci.vehicle.getPosition(vehString)[0])
            save = save + " " + str(gap)
        f2.write(str(step/100)+save+"\n")
        save = ""
        for i in range(10):
            vehString = "veh"+str(i)
            gap = str(traci.vehicle.getPosition(vehString)[0])
            save = save + " " + str(gap)
        f3.write(str(step/100)+save+"\n")

    step += 1

traci.close()
