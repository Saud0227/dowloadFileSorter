import os
import pathlib as p
import time as t
import datetime
from typing_extensions import runtime

active = True
runtime=0

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
    t.sleep(600)


# rpyc servic definition



# import rpyc

# class MyService(rpyc.Service):
#     def exposed_toggle(self, function = lambda x: x):
#         return main.testthings(function = function)
#     def exposed_runtime(self):
#         return runtime

# # start the rpyc server
# from rpyc.utils.server import ThreadedServer
# from threading import Thread
# server = ThreadedServer(MyService, port = 12345)
# t = Thread(target = server.start)
# t.daemon = True
# t.start()




def toggle(_input):
    global avtive
    if isinstance(_input, bool):
        avtive = _input
    else:
        return active













while True:
    runtime+=1
    if active:
        mainloop()