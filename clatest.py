import traci
import os
import math
import numpy as np
import random
from decimal import Decimal
from sympy import *
import threading
import time

x = Symbol('x')


def calRiskBySpeed(nowSpeed, frontSpeed, maxBrake, notice, expect):
    solve_value = solve([((nowSpeed**2 * maxBrake)/(frontSpeed**2 +
                        2*maxBrake*(x - nowSpeed * notice)) / maxBrake) - expect], [x])
    return solve_value


def calACC(t):
    solve_value = solve([(460-500+30)+(0.5*x*(t**2))], [x])
    return solve_value


def calACCSpeedDiff(nowSpeed, frontSpeed,t):
    solve_value = solve([(-10-46.0)-(nowSpeed-frontSpeed)*t+(0.5*x*(t**2))], [x])
    return solve_value


print(calRiskBySpeed(30,30,8,1.5,1))


# 3.2833999999852495

time = 100
nowSpeed = 20
frontSpeed = 12
a = calACCSpeedDiff(nowSpeed,frontSpeed,time)
if ":" in str(a):
    characters = "{x:}"
    tempString = str(a)
    for j in range(len(characters)):
        tempString = tempString.replace(characters[j], "")
    a = float(tempString)
ans = nowSpeed - a*time
print("dec is: "+str(a))
print(ans)



# dec = - ((450-500 +11.5) - ((15 - 20)* time)) /  (time ** 2 * 0.5)
# print(dec)


# a = calACC(time)
# if ":" in str(a):
#     characters = "{x:}"
#     tempString = str(a)
#     for j in range(len(characters)):
#         tempString = tempString.replace(characters[j], "")
#     a = float(tempString)
# ans = 20 - a*time
# print("dec is: "+str(a))
# print(ans)
