# This version executes main program with a console window 
# and is used to see aditional information and usfull
# for debugging


import os
import pathlib as p
import time as t
import datetime
from sys import exit
from plyer import notification
# from typing_extensions import runtime

active = True
# Checks files while true
runtime=0
# Number of times main loop has run, 1/sec
tToCheck=10
# Checks for files at 0
cc=0
# Number of checks the program has done
sh=False
# When true, the program shutsdown the next loop

pa = p.Path.home()
tDir = pa / "Downloads"
# C:\Users\CarlJ\Downloads
sufix = [".zip"]


def checkFold():
    dirC=[]
    for i in sufix:
        if p.Path.is_dir(tDir / i[1:]) is False:
            os.mkdir(i[1:])
            dirC.append(tDir / i[1:])
    for j in dirC:
        print(str(j) + " was created")

os.chdir(tDir)




def mainloop():
    nFSorted=0
    filesToSort = [f for f in os.listdir(tDir) if p.Path( tDir / f ).is_file()]
    for fil in filesToSort:
        fP=p.Path(tDir / fil)
        fSufix = fP.suffix
        if(fSufix not in sufix):
            sufix.append(fSufix)
        checkFold()
        fts=fP.stat().st_ctime
        fTS=datetime.datetime.fromtimestamp(fts)
        cT=datetime.datetime.today()
        difT = cT - fTS
        if difT.days>3:
            os.rename(str(fP),str(tDir / fSufix[1:] / fP.parts[-1]))
            nFSorted+=1
    if nFSorted<0:
        sendNot(str(nFSorted) + " files were sorted.")

# rpyc servic definition


def toggle(_input):
    global active
    # print("\nActive")
    # print(active, type(active))
    # print("\nInput")
    # print(_input, type(_input))
    # print("\nAre they the same?")
    # print(active == _input)
    # print("\n")

    if isinstance(_input, bool) and active != _input:
        active = _input
        if active:
            sendNot("Download sorter resumed work", 10)
        else:
            sendNot("Download sorter paused",10)
        return("status: " + str(active))
    elif active == _input:
        return ("Status is allready set to " + str(active))
    else:
        return active


import rpyc

class MyService(rpyc.Service):
    def exposed_toggleRun(self,_arg):
        global active, sh

        # print("Toggle run is called with arg: " + _arg)
        
        if _arg == "true" or _arg == "false":
            if _arg == "true":
                return(toggle(True))
            elif _arg == "false":
                return(toggle(False))
        else:
            return (active)
    def exposed_runtime(self):
        global active
        return [runtime, cc]
    def exposed_close(self):
        global sh
        sh = True
        sendNot("Dowload sorter procsess aborted", 50)




print("Starting rpyc")
# start the rpyc server
from rpyc.utils.server import ThreadedServer
from threading import Thread
server = ThreadedServer(MyService, port = 12345)
th = Thread(target = server.start)
th.daemon = True
th.start()
print("rpyc started")


def sendNot(_text, _time):
    if not isinstance(_time, (float,int)) and _time < 10:
        _time = 10
    notification.notify(title = "Dowload Sorter", message = _text, timeout = _time)

sendNot("Dowload sorter initiated",10)
while True:
    if sh:
        exit()
    runtime+=1
    tToCheck-=1
    if active and tToCheck<=0:
        mainloop()
        cc+=1
        tToCheck=100
    print(runtime,active)
    # active= not active
    t.sleep(1)


# cd Desktop\Projects\python\downloadFileSorter