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

# 開檔案
f = 0
f2= 0
f3 = 0

# 停止換車道參數
stopChangeFlag = 0

# 車輛長度與數量
carLength = 4
carNumber = 10

# 車間距離變數
space = []
# 車間距離數量
matrixLength = 0
spaceMatrix = []
fleetMatrix = []

# 計算空間排序變數
miniIndex = []
miniIndexSpace = []
miniIndexSpaceCount = []
mappingStartEndSorting = []

# 安全距離(舊)
safeSpce = 5

#重新計算Flag
restartFlag = 0 

# 新安全距離(跟車風險為1時)
safeDistace = []
selectdone = []

#車隊車速
fleetSpeed = [] 

# 計算所需空間(舊)
changeNeedSpace = np.zeros(10)

#滿足空間 
satisSpace = []
satisTmp = []

#滿足空間號碼 
satisSpaceNumber = []
newSatisSpaceNumber = []

# 空間開始到結束
startEndSpace = []
mappingStartEnd = []

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

minSatiSpace = 0
minSatirange = ""

# 計算單個空間可以放幾台車
spaceCarCount = []

# 車子分配到那一個空間
carAssignSpace = []

# inital function start
# 寫檔初始化
def writeInit():
    global f, f2,f3
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

# 初始化車子分配空間
def initCarAssign():
    global carAssignSpace
    for i in range(10):
        carAssignSpace.append(-1)

# 初始化車輛位置(不只位置)
def initPosition():
    global fleetPosition, otherPosition, fleetLandID, otherLandID, saftyDistace, fleetSpeed
    for i in range(11):
        fleetPosition.append(0)
        otherPosition.append(0)
        fleetLandID.append(-1)
        otherLandID.append(-1)
        safeDistace.append(-1)
        fleetSpeed.append(0)
        selectdone.append(0)

# old 換車道所需空間
def staticChangeSpace():
    for i in range(carNumber):
        changeNeedSpace[i] = (i + 1) * (carLength + safeSpce)

#初始化changeFlag  
def changeInit():
    for i in range(11):
        changeFlag.append(0)

# 車隊車速初始化
def speedInit():
    for i in range(11):
        vehString3 = "veh"+str(i)
        traci.vehicle.setSpeed(vehString3, 20)
    traci.vehicle.setSpeed("stop", 0)

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

# 設定非車隊換車道模式
def noNoChange():
    for i in range(12):
        no = "no" + str(i)
        traci.vehicle.setLaneChangeMode(no, 0b000000000000)

# 設定車隊換車道模式
def fleetNoChange():
    for i in range(11):
        veh = "veh" + str(i)
        traci.vehicle.setLaneChangeMode(veh, 0b000000000000)

# 設定車隊車輛速度模式
def speedModeInit():
    speedMode = 0
    for i in range(11):
        veh = "veh" + str(i)
        traci.vehicle.setSpeedMode(veh, speedMode)

# 空間放入矩陣
def getSpace():
    for i in range(10):
        no = "no"+str(i)
        no2 = "no"+str(i+1)
        gap = traci.vehicle.getPosition(no)[0] - traci.vehicle.getPosition(no2)[0]
        space[i] = gap

#取得車隊長度
def getFleetLength():

    # fleetLength = 0 
    # for i in range(0, 10):
    #     veh = "veh" + str(i)
    #     veh2 = "veh" + str(i+1)
    #     frontSpeed = traci.vehicle.getSpeed(veh)
    #     nowSpeed = traci.vehicle.getSpeed(veh2)
    #     notice = 0.1
    #     solve_value = calRiskBySpeed(nowSpeed, frontSpeed, 8, notice, 1)
    #     if ":" in str(solve_value):
    #         characters = "{,x:}"
    #         tempString = str(solve_value)
    #     for j in range(len(characters)):
    #         tempString = tempString.replace(characters[j], "")
    #     saftyDistace = float(tempString)
    #     fleetLength = fleetLength + saftyDistace
    #     fleetLength = fleetLength + 4
    # fleetLast = fleetLength + safeSpce
    # return fleetLength
    veh = "veh" + str(0)
    veh2 = "veh" + str(10)
    fleetLength = traci.vehicle.getPosition(veh)[0] - traci.vehicle.getPosition(veh2)[0] + 4
    print(fleetLength);
    return fleetLength
    
# 計算取得安全距離
def calculateSafeDistance():
    global saftyDistace
    for i in range(0, 10):
        veh = "veh"+str(i)
        veh2 = "veh"+str(i+1)
        nowSpeed = traci.vehicle.getSpeed(veh2)
        frontSpeed = traci.vehicle.getSpeed(veh)

        if nowSpeed != fleetSpeed[i+1] or  frontSpeed != fleetSpeed[i]:
            fleetSpeed[i+1] = nowSpeed
            fleetSpeed[i] = frontSpeed
            solve_value = calRiskBySpeed(nowSpeed, frontSpeed, 8, 0.1, 1)
            if ":" in str(solve_value):
                characters = "{,x:}"
                tempString = str(solve_value)
                for j in range(len(characters)):
                    tempString = tempString.replace(characters[j], "")
                safty= float(tempString)
                safeDistace[i] = safty
    print(safeDistace)
    



# 填滿矩陣空間
def calMatrixSpace():
    global matrixLength
    for i in range(matrixLength):
        for j in range(matrixLength):
            if i == j:
                spaceMatrix[i,j] = space[i]
                startEndSpace[i][j] = str(i) + "-" + str(j)
            else:
                if i > j:
                    start = j
                    end = i
                    tmp = 0
                    for k in range(start,end+1):
                        tmp = tmp + space[k]
                    spaceMatrix[i,j] = tmp
                    startEndSpace[i][j] = str(start) + "-" + str(end)
                    tmp = 0
                else:
                    start = i
                    end = j
                    tmp = 0
                    for k in range(start,end+1):
                        tmp = tmp + space[k]
                    spaceMatrix[i,j] = tmp
                    startEndSpace[i][j] = str(start) + "-" + str(end)
                    tmp = 0
    # print(spaceMatrix)

# 空間符合車隊長度
def calFitFleetSpace(fleetLast):
    for i in range(matrixLength):
        for j in range(matrixLength):
            if spaceMatrix[i, j] > fleetLast + 0 * (carLength + safeSpce):
                # print(spaceMatrix[i, j])
                satisSpace.append(spaceMatrix[i, j])
                satisSpaceNumber.append(abs(i - j) + 1)
                satisTmp.append(abs(i - j) + 1)
                newSatisSpaceNumber.append(abs(i - j) + 1)
                mappingStartEnd.append(startEndSpace[i][j])
    print(satisSpace)
    print("\n")

# 空間排序
def sortingSpace():
    global minSatiSpace, minSatirange
    minSatisSpaceNumber = min(newSatisSpaceNumber)
    print(minSatisSpaceNumber)
    minSatiSpace = 0
    minSatirange = ""
    for i in range(len(newSatisSpaceNumber)):
        if newSatisSpaceNumber[i] == minSatisSpaceNumber:
            if minSatiSpace == 0:
                minSatiSpace = satisSpace[i]
                minSatirange = mappingStartEnd[i]
            elif minSatiSpace >satisSpace[i]:
                minSatiSpace = satisSpace[i]
                minSatirange = mappingStartEnd[i]
    # print(minSatiSpace)
    # print(minSatirange)
    
    



    # while min(satisTmp) != 10000:
    #     for i in range(len(satisTmp)):
    #         if satisSpaceNumber[i] == min(satisTmp):
    #             miniIndex.append(i)
    #             miniIndexSpace.append(satisSpace[i])
    #             mappingStartEndSorting.append(mappingStartEnd[i])
    #             satisTmp[i] = 10000
    # newSatisSpaceNumber.sort() 

    # print(miniIndexSpace)
    # print("\n")
    # print(mappingStartEndSorting)
    # print("\n")
    # print(newSatisSpaceNumber)

    # print(len(satisSpace))
    
    satisSpace.clear()
    satisSpaceNumber.clear()
    newSatisSpaceNumber.clear()
    mappingStartEnd.clear()
    satisTmp.clear()

# 選擇最小的空間
def sortingMiniChoose():
    global restartFlag, minSatirange, spaceCarCount, matrixLength
    chooseSpace = []
    spaceCarCount.clear()
    start, end = minSatirange.split("-")
    # print("matrixLength: "+str(matrixLength))

    if restartFlag == 0:
        start = int(start)
        end = int(end)
    elif restartFlag == 1:
        if int(end) + 1 > matrixLength - 1:
            start = int(start) + 1
            end = int(end)
            minSatirange = str(start) + "-"+ str(end)
        else:
            start = int(start)
            end = int(end) + 1
            minSatirange = str(start) + "-"+ str(end)
    restartFlag = 0

    for i in range(start,end+1):
        chooseSpace.append(space[i])
    print(chooseSpace)
    
    # fleetMatrix
    for i in range(len(chooseSpace)):
        if countAll(spaceCarCount) > carNumber:
            break
        for j in range(10):

            if start == end:
                tmp = carNumber-(countAll(spaceCarCount))
                spaceCarCount.append(tmp)
                break
                
            elif chooseSpace[i] >= changeNeedSpace[j] and chooseSpace[i] < changeNeedSpace[j+1]:
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
    if(countAll(spaceCarCount) < carNumber):
        restartFlag = 1;
        sortingMiniChoose()
    else:
        print(minSatirange)
        print(countAll(spaceCarCount))
        print(spaceCarCount)
    # print("dfssfdsf"+str(chooseSpace)

# 計算array累加
def countAll(list):
    tmp = 0
    for i in range(len(list)):
        tmp = tmp + list[i]
    return tmp

# 分配車輛到指定空間
def carFittingSpace():
    start, end = minSatirange.split("-")
    start = int(start)
    end = int(end)
    count = 0
    whichCount = 0
    for i in range(len(spaceCarCount)):
        while count != spaceCarCount[i]:
            carAssignSpace[whichCount] = i + start
            whichCount = whichCount + 1
            count = count + 1
        count = 0
    print(carAssignSpace)
            
        
        

        


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

# normal python
# 空間初始化
def spaceInit():
    global matrixLength, spaceMatrix, startEndSpace, fleetMatrix
    for i in range(10):
        space.append(0)
    # 空間矩陣初始化
    matrixLength = np.size(space)
    spaceMatrix = np.empty((matrixLength, matrixLength))
    fleetMatrix = np.empty((matrixLength, matrixLength))
    startEndSpace = [["1" for _ in range(matrixLength)] for _ in range(matrixLength)]


def fleetCalculatePosition():
    vehPosition = traci.vehicle.getPosition("veh0")[0]
    vehPosition2 = traci.vehicle.getPosition("veh10")[0]
    allLength = abs(vehPosition - vehPosition2)+carLength
    return allLength


# 車隊所需空間大小
def fleetCalculate():
    global matrixLength, fleetMatrix
    for i in range(matrixLength):
        for j in range(matrixLength):
            veh = "veh" + str(i)
            veh1 = "veh" + str(j)
            vehPosition = traci.vehicle.getPosition(veh)[0]
            vehPosition1 = traci.vehicle.getPosition(veh1)[0]
            if i == j:
                fleetMatrix[i, j] = carLength + safeDistace[i]

            elif i > j:
                start = j
                end = i
                tmp = 0
                for k in range(start,end+1):
                    tmp = tmp + carLength + safeDistace[k]
                fleetMatrix[i, j] = tmp

            elif  i < j:
                start = i
                end = j
                tmp = 0
                for k in range(start,end+1):
                    tmp = tmp + carLength + safeDistace[k]
                fleetMatrix[i, j] = tmp
                # fleetMatrix[i, j] = int(abs(vehPosition - vehPosition1) + carLength + safeSpce)
    print (fleetMatrix)




# changeNeedSpace = np.zeros(10)
# satisSpace = []
# satisTmp = []
# satisSpaceNumber = []
# newSatisSpaceNumber = []
# startEndSpace = [["1" for _ in range(matrixLength)]
#                  for _ in range(matrixLength)]
# mappingStartEnd = []

# for i in range(carNumber):
#     changeNeedSpace[i] = (i + 1) * (carLength + safeSpce)

# print(changeNeedSpace)
# print("\n")


# for i in range(matrixLength):
#    for j in range(matrixLength):
#       spaceMatrix[i,j] = 0

# for i in range(matrixLength):
#    spaceMatrix[i,i] = space[i]



# count = 0
# for i in range(matrixLength):
#     for j in range(matrixLength):
#         if spaceMatrix[i, j] > fleetLast + 0 * (carLength + safeSpce):
#             satisSpace.append(spaceMatrix[i, j])
#             satisSpaceNumber.append(abs(i - j) + 1)
#             satisTmp.append(abs(i - j) + 1)
#             newSatisSpaceNumber.append(abs(i - j) + 1)
#             mappingStartEnd.append(startEndSpace[i][j])



# print(satisSpace)
# print("\n")
# print(satisSpaceNumber)
# print("\n")
# print(startEndSpace)
# print("\n")
# print(mappingStartEnd)
# print("\n")

# if min(satisSpaceNumber)


#////////////////////////////

# miniIndex = []
# miniIndexSpace = []
# miniIndexSpaceCount = []
# mappingStartEndSorting = []

# while min(satisTmp) != 10000:
#     for i in range(len(satisTmp)):
#         if satisSpaceNumber[i] == min(satisTmp):
#             miniIndex.append(i)
#             miniIndexSpace.append(satisSpace[i])
#             mappingStartEndSorting.append(mappingStartEnd[i])
#             satisTmp[i] = 10000

# newSatisSpaceNumber.sort()

# print(miniIndexSpace)
# print("\n")
# print(mappingStartEndSorting)
# print("\n")
# print(newSatisSpaceNumber)


# # Splitting fleet to group

# # Chooose mini of sorting matrix
# chooseSpace = []
# spaceCarCount = []
# start, end = mappingStartEndSorting[0].split("-")
# start = int(start)
# end = int(end)
# for i in range(start, end+1):
#     chooseSpace.append(space[i])

# print(chooseSpace)


# def countAll(list):
#     tmp = 0
#     for i in range(len(list)):
#         tmp = tmp + list[i]
#     return tmp


# for i in range(len(chooseSpace)):
#     if countAll(spaceCarCount) > carNumber:
#         break
#     for j in range(len(changeNeedSpace)):
#         if chooseSpace[i] >= changeNeedSpace[j] and chooseSpace[i] < changeNeedSpace[j+1]:
#             if countAll(spaceCarCount)+(j+1) > carNumber:
#                 tmp = carNumber-(countAll(spaceCarCount))
#                 spaceCarCount.append(tmp)
#                 if tmp != 0:
#                     chooseSpace[i] = chooseSpace[i]-changeNeedSpace[tmp]
#                 break
#             else:
#                 spaceCarCount.append(j+1)
#                 chooseSpace[i] = chooseSpace[i]-changeNeedSpace[j]
#                 break

# print(spaceCarCount)
# print(chooseSpace)




def startSimulate():
    global step
    global f, f2,f3
    global stopChangeFlag
    while step < 40000:
        traci.simulationStep()
        if step == 0:
            staticChangeSpace()
            initPosition()
            initCarAssign()
            changeInit()
            speedInit()
            changeTime()
            noNoChange()
            fleetNoChange()
            speedModeInit()
            writeInit()
            spaceInit()

        if step > 0:
            calculateSafeDistance()
            getAllPosition()
            getAllLaneID()
            getSpace()
            calMatrixSpace()
            fleetCalculate()
            calFitFleetSpace(fleetMatrix[0, 9])
            # calFitFleetSpace(fleetCalculatePosition())
            sortingSpace()
            sortingMiniChoose()
            carFittingSpace()
            riskFollowing()
            

        if step == 1:
            for i in range(10):
                vehString = "veh"+str(i+1)
                traci.vehicle.setSpeed(vehString, 30)

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

                    # if i == 10:
                    #     print ("gap: " + str(gap))
                    #     print ("safetyDistace: " + str(safetyDistace))
                    #     print ("gap + frontSlideDistace: " + str(gap + frontSlideDistace))
                    #     print ("nowSpeed * 1.5: " + str(nowSpeed * 1.5))
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

            




if __name__ == "__main__":
    startSimulate()
    print("fsdf")