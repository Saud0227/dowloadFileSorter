import os
import pathlib as p
import time as t
import datetime
from sys import exit
# from typing_extensions import runtime

active = True
runtime=0
sh=False

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
        print(nFSorted)

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
        
        if _arg == "True" or _arg == "False":
            if _arg == "True":
                return(toggle(True))
            elif _arg == "False":
                return(toggle(False))
        else:
            return (active)
    def exposed_runtime(self):
        global active
        return [runtime, active]
    def exposed_close(self):
        global sh
        sh = True
        print("!!!")




print("Starting rpyc")
# start the rpyc server
from rpyc.utils.server import ThreadedServer
from threading import Thread
server = ThreadedServer(MyService, port = 12345)
th = Thread(target = server.start)
th.daemon = True
th.start()
print("rpyc started")




print("Starting mainloop")
while True:
    if sh:
        exit()
    runtime+=1
    if active:
        mainloop()
    print(runtime,active)
    # active= not active
    t.sleep(10)


# cd Desktop\Projects\python\downloadFileSorter