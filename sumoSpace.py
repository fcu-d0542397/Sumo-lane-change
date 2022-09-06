import traci
import os
import math
import numpy as np
import random
from decimal import Decimal
from sympy import *
import threading
import time

sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c",
           "C:\\Users\\user\\Desktop\\sumo\\laneChange\\space\\myConfig.sumocfg"]
traci.start(sumoCmd)

# traci start

# 變數宣告
step = 0
allAre1 = 0

# 計算風險安全距離
x = Symbol('x')

# 車輛座標位置
fleetPosition = []
otherPosition = []

# 車輛id
fleetLandID = []
otherLandID = []

# 是否完成切換車道
changeFlag = []

# 開始切換速度的時間
changeSpeedTime = []

# inital function start
# 初始化車輛位置
def initPosition():
    for i in range(11):
        fleetPosition.append(0)
        otherPosition.append(0)
        fleetLandID.append(-1)
        otherLandID.append(-1)

#初始化changeFlag  
def changeInit():
    for i in range(11):
        changeFlag.append(0)

# 車隊車速初始化
def speedInit():
    for i in range(11):
        vehString3 = "veh"+str(i)
        traci.vehicle.setSpeed(vehString3, 20)

# 變換車道時間初始化
def changeTime():
    for i in range(11):
        changeSpeedTime.append(-1)

# inital function end

# function start
# 計算跟車風險(跟車加速度)
def calFollowSpeed(nowSpeed, frontSpeed, distance, notice, brakeMax):
    follow = (nowSpeed**2 * brakeMax) / (frontSpeed**2 +
                                         2 * brakeMax * (distance - nowSpeed * notice))
    return follow

# 計算跟車安全距離
def calRiskBySpeed(nowSpeed, frontSpeed, maxBrake, notice, expect):
    solve_value = solve([((nowSpeed**2 * maxBrake)/(frontSpeed**2 +
                        2*maxBrake*(x - nowSpeed * notice)) / maxBrake) - expect], [x])
    return solve_value

# 計算緊急煞車滑行距離
def calSlideDistace(speed, maxBrake, time):
    slideDistace = speed * time - 0.5 * maxBrake * (time**2)
    return slideDistace

# 取得車輛行駛車道
def getAllLaneID():
    for i in range(11):
        veh = "veh" + str(i)
        no = "no" + str(i)
        fleetLandID[i] = traci.vehicle.getLaneIndex(veh)
        otherLandID[i] = traci.vehicle.getLaneIndex(no)

# 取得車輛位置
def getAllPosition():
    for i in range(11):
        veh = "veh" + str(i)
        no = "no" + str(i)
        fleetPosition[i] = traci.vehicle.getPosition(veh)[0]
        otherPosition[i] = traci.vehicle.getPosition(no)[0]

# 計算最近跟車車輛
def calClosestCar(now, index):
    # 當前車輛車道位置
    landID = traci.vehicle.getLaneIndex(now)
    # 當前車輛位置
    nowPosition = traci.vehicle.getPosition(now)[0]
    min = -1
    minIndex = 0
    # 是不是車隊車車輛
    fleetOrNot = -1
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

# 設定換車道模式
def noNoChange():
    for i in range(12):
        no = "no" + str(i)
        traci.vehicle.setLaneChangeMode(no, 0b000000000000)

# 設定車隊車輛速度模式
def speedModeInit():
    speedMode = 0
    for i in range(12):
        veh = "veh" + str(i)
        traci.vehicle.setSpeedMode(veh, speedMode)

# 風險檢測
def riskFollowing():

    # 檢查flag
    global allAre1
    allAre1 = 0

    # 判斷前方車輛的種類
    for i in range(1, 11):
        now = "veh"+str(i)
        front = "veh"+str(i-1)
        closeset = calClosestCar(now, i)
        if closeset[0] == 0:
            front = "no"+str(closeset[1])
        elif closeset[0] == 1:
            front = "veh"+str(closeset[1])
        if "no" in front:
            notice = 1.5
        elif "no" in now:
            notice = 1.5
        elif "veh" in now and  "veh" in front:
            notice = 0.1

        # 取得車輛速度
        frontSpeed = traci.vehicle.getSpeed(front)
        nowSpeed = traci.vehicle.getSpeed(now)
        # 車與車之間x座標之距離
        gap = traci.vehicle.getPosition(front)[0] - traci.vehicle.getPosition(now)[0] - 4
        # 計算理當前理想的跟車速度
        acci = calFollowSpeed(nowSpeed, frontSpeed, gap, notice, 8)
        
        # 計算單前風險值
        followRisk = acci / 8

        # 風險值大於1之情況
        if abs(followRisk) >= 1:
            solve_value = calRiskBySpeed(nowSpeed, frontSpeed, 8, notice, 1)
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

            # 以最大度進行減速
            if saftyDistace > gap:
                oneSpeed = 8 / 10
                if traci.vehicle.getSpeed(now) - oneSpeed > 0:
                    newSpeed = traci.vehicle.getSpeed(now) - oneSpeed
                    traci.vehicle.setSpeed(now, newSpeed)
                    if i == 9:
                        print("oneSpeed : " +str(oneSpeed))
                        print("newSpeed : " +str(newSpeed))

            # # 計算合理的減速度
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
# traci end


space = []
for i in range(10):
    space.append(random.randint(9, 27))

matrixLength = np.size(space)
spaceMatrix = np.empty((matrixLength, matrixLength))
carLength = 4
carNumber = 10
safeSpce = 5
fleetLength = 4 * carNumber + (carNumber - 1) * safeSpce
fleetLast = fleetLength + safeSpce

changeNeedSpace = np.zeros(10)
satisSpace = []
satisTmp = []
satisSpaceNumber = []
newSatisSpaceNumber = []
startEndSpace = [["1" for _ in range(matrixLength)]
                 for _ in range(matrixLength)]
mappingStartEnd = []

for i in range(carNumber):
    changeNeedSpace[i] = (i + 1) * (carLength + safeSpce)

print(changeNeedSpace)
print("\n")


# for i in range(matrixLength):
#    for j in range(matrixLength):
#       spaceMatrix[i,j] = 0

# for i in range(matrixLength):
#    spaceMatrix[i,i] = space[i]

for i in range(matrixLength):
    for j in range(matrixLength):
        if i == j:
            spaceMatrix[i, j] = space[i]
            startEndSpace[i][j] = str(i) + "-" + str(j)
        else:
            if i > j:
                start = j
                end = i
                tmp = 0
                for k in range(start, end+1):
                    tmp = tmp + space[k]
                spaceMatrix[i, j] = tmp
                startEndSpace[i][j] = str(start) + "-" + str(end)
                tmp = 0
            else:
                start = i
                end = j
                tmp = 0
                for k in range(start, end+1):
                    tmp = tmp + space[k]
                spaceMatrix[i, j] = tmp
                startEndSpace[i][j] = str(start) + "-" + str(end)
                tmp = 0

print(spaceMatrix)
print("\n")

count = 0
for i in range(matrixLength):
    for j in range(matrixLength):
        if spaceMatrix[i, j] > fleetLast + 0 * (carLength + safeSpce):
            satisSpace.append(spaceMatrix[i, j])
            satisSpaceNumber.append(abs(i - j) + 1)
            satisTmp.append(abs(i - j) + 1)
            newSatisSpaceNumber.append(abs(i - j) + 1)
            mappingStartEnd.append(startEndSpace[i][j])

# print(satisSpace)
# print("\n")
# print(satisSpaceNumber)
# print("\n")
# print(startEndSpace)
# print("\n")
# print(mappingStartEnd)
# print("\n")

# if min(satisSpaceNumber)
miniIndex = []
miniIndexSpace = []
miniIndexSpaceCount = []
mappingStartEndSorting = []

while min(satisTmp) != 10000:
    for i in range(len(satisTmp)):
        if satisSpaceNumber[i] == min(satisTmp):
            miniIndex.append(i)
            miniIndexSpace.append(satisSpace[i])
            mappingStartEndSorting.append(mappingStartEnd[i])
            satisTmp[i] = 10000

newSatisSpaceNumber.sort()

print(miniIndexSpace)
print("\n")
print(mappingStartEndSorting)
print("\n")
print(newSatisSpaceNumber)


# Splitting fleet to group

# Chooose mini of sorting matrix
chooseSpace = []
spaceCarCount = []
start, end = mappingStartEndSorting[0].split("-")
start = int(start)
end = int(end)
for i in range(start, end+1):
    chooseSpace.append(space[i])

print(chooseSpace)


def countAll(list):
    tmp = 0
    for i in range(len(list)):
        tmp = tmp + list[i]
    return tmp


for i in range(len(chooseSpace)):
    if countAll(spaceCarCount) > carNumber:
        break
    for j in range(len(changeNeedSpace)):
        if chooseSpace[i] >= changeNeedSpace[j] and chooseSpace[i] < changeNeedSpace[j+1]:
            if countAll(spaceCarCount)+(j+1) > carNumber:
                tmp = carNumber-(countAll(spaceCarCount))
                spaceCarCount.append(tmp)
                if tmp != 0:
                    chooseSpace[i] = chooseSpace[i]-changeNeedSpace[tmp]
                break
            else:
                spaceCarCount.append(j+1)
                chooseSpace[i] = chooseSpace[i]-changeNeedSpace[j]
                break

print(spaceCarCount)
print(chooseSpace)



if __name__ == "__main__":
    print("fsdf")