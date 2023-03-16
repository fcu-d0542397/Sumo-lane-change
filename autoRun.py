import sumoSpaceAuto as ssa
from datetime import datetime
import asyncio
import time


def run():
    speed = [16.66,19.4,22.2,25,27,30]
    for i in range(4,10):
        for j in range(len(speed)):
            timeNow =  datetime.now()
            currentTime =  timeNow.strftime("%m-%d-%H-%M")
            saveName1 =  "./"+str(currentTime) + "-speed-" + str(speed[j]) + "-space-"+str(i)+"-fleetSpeed.txt"
            saveName2 =  "./"+str(currentTime) + "-speed-" + str(speed[j]) + "-space-"+str(i)+"-noFleetSpeed.txt"
            saveName3 =  "./"+str(currentTime) + "-speed-" + str(speed[j]) + "-space-"+str(i)+"-group.txt"
            # print("\n"+currentTime)

            ssa.startSimulate(speed[j] , i,saveName1,saveName2,saveName3)
            time.sleep(10)

            # task1 = asyncio.create_task(ssa.startSimulate(speed[j] , i,saveName1,saveName2)) 
            # ssa.startSimulate(speed[j] , i,saveName1,saveName2)
            # task1
            # asyncio.sleep(10) 


if __name__ == "__main__":
    run()
    # a = asyncio.run(run())
    # speed = [16.66,19.4,22.2,25,27,30]
    # for i in range(10):
    #     for j in range(len(speed)):
    #         timeNow = datetime.now()
    #         currentTime = timeNow.strftime("%Y-%m-%d-%H-%M")
    #         saveName1 = "./"+str(currentTime) + "-speed-" + str(speed[j]) + "-space-"+str(i)+"-fleetSpeed.txt"
    #         saveName2 = "./"+str(currentTime) + "-speed-" + str(speed[j]) + "-space-"+str(i)+"-noFleetSpeed.txt"
    #         print("\n"+currentTime)
    #         asyncio.run(asyncio.wait(ssa.startSimulate(speed[j] , i,saveName1,saveName2)))
    #         await asyncio.sleep(10) 


