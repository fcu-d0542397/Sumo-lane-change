import math
import os
import traci
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
    traci.vehicle.setSpeedMode("veh0", 0)
    traci.vehicle.setSpeedMode("veh1", 0)
    traci.vehicle.setSpeedMode("veh2", 0)
    traci.vehicle.setSpeedMode("veh3", 0)

    traci.vehicle.setSpeedMode("veh4", 0)
    traci.vehicle.setSpeedMode("veh5", 0)
    traci.vehicle.setSpeedMode("veh6", 0)
    traci.vehicle.setSpeedMode("veh7", 0)

    traci.vehicle.setSpeedMode("veh8", 0)
    traci.vehicle.setSpeedMode("veh9", 0)
    traci.vehicle.setSpeedMode("veh10", 0)
    traci.vehicle.setSpeedMode("veh11", 0)


def changeInit():
    for i in range(11):
        changeFlag.append(0)


def speedInit():
    for i in range(11):
        vehString3 = "veh"+str(i)
        # no = "no"+str(i)
        traci.vehicle.setSpeed(vehString3, 30)
        # traci.vehicle.setSpeed(no, 10)


def changeTime():
    for i in range(11):
        changeSpeedTime.append(-1)


def initZoomFlag():
    for i in range(10):
        zoomOut.append(-1)


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

    # if step > 0 and step % 100 == 0:
    #    calSpace()

    if step == 0:
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

    veh0 = traci.vehicle.getPosition("veh0")
    veh11 = traci.vehicle.getPosition("veh11")

    # if step == 1000:
    #    # traci.vehicle.changeLane("veh1", 1, 300)
    #    for i in range(11):
    #       tmp = "no" + str(i)
    #       traci.vehicle.setSpeed(tmp, 0)

    # if step == 3000:
    #    for i in range(11):
    #       veh = "veh" + str(i)
    #       traci.vehicle.setSpeed(veh, 20)

    if step == 2000:
        for i in range(10):
            vehString = "veh"+str(i+1)
            traci.vehicle.setSpeed(vehString, 30)

    if step > 2000:
        for i in range(10):
            front = "veh"+str(i)
            back = "veh" + str(i+1)
            if traci.vehicle.getPosition(front)[0]-traci.vehicle.getPosition(back)[0] > 40:
               traci.vehicle.setSpeed(back, -1)


    # if step > 2000 and stopChangeFlag < 11:
    #    for i in range(11):
    #       veh = "veh" + str(i)
    #       no = "no" + str(i)
    #       if traci.vehicle.getPosition(no)[0]-traci.vehicle.getPosition(veh)[0] < 60 and changeFlag[i] == 0:
    #          traci.vehicle.changeLane(veh, 1, 300)
    #          changeFlag[i] = 1
    #          changeSpeedTime[i] = step + 150
    #          stopChangeFlag = stopChangeFlag + 1
    #          # traci.vehicle.setSpeed(veh, -1)

    # if step > 2000 and  allChangeFlag == -1:
    #    for i in range(11):
    #       if step == changeSpeedTime[i]:
    #          veh = "veh" + str(i)
    #          no = "no" + str(i)
    #          print("now changing"+ str(i))
    #          traci.vehicle.setSpeed(veh, traci.vehicle.getSpeed(no))
    #          traci.vehicle.setSpeed(veh, traci.vehicle.getSpeed(no))
    #    if -1 in changeSpeedTime == False:
    #       allChangeFlag = 0

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
