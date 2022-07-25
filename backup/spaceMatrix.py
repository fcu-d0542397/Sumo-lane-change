import traci
import os
import math
import numpy as np
import random

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
startEndSpace = [["1" for _ in range(matrixLength)] for _ in range(matrixLength)]
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
for i in range(start,end+1):
   chooseSpace.append(space[i])

print(chooseSpace)


def countAll(list):
   tmp = 0
   for i in range(len(list)):
      tmp = tmp +list[i]
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


