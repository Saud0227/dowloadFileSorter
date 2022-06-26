# This version executes main program in background
# and is the preferred way to run the program


import os
import pathlib as p
import time as t
import datetime
from sys import exit

#RPyC imports
from rpyc.utils.server import ThreadedServer
from threading import Thread

import logging
logging.basicConfig(filename='app.log', format='%(asctime)s - %(message)s', level=logging.INFO)


# Checks files while true
active = True

# Number of times main loop has run, 1/sec
runtime = 0

# Checks for files at 0
tToCheck = 10

# Number of checks the program has done
cc = 0

# When true, the program shutdown the next loop
sh = False

# When false, sort all items regardless of when they
# were created. This flag is kept at false unless
# executed via command from secondary application
forceCheckFlag = False


logP = p.Path.cwd() / 'logFiles'
if p.Path.is_dir(logP) is False:
    os.mkdir('logFiles')
    logging.warning(f'Made logFiles dir at {logP}')


tDir = p.Path.home() / "Downloads"
# C:\Users\CarlJ\Downloads
suffix = [".zip"]


def checkFold():
    dirC=[]
    for i in suffix:
        if p.Path.is_dir(tDir / i[1:]) is False:
            os.mkdir(i[1:])
            dirC.append(tDir / i[1:])
    for j in dirC:
        logging.info(str(j) + " was created")

os.chdir(tDir)


def writeOutputFiles(toWrite):
    global logP
    timeStamp = str(datetime.datetime.now()).split('.')[0].split()

    hhMMss = timeStamp[1].split(':')
    timeStamp[1] = ''.join(hhMMss[0] + '.' + hhMMss[1])

    nameSpace = ''.join(timeStamp[0] + '_' + timeStamp[1])

    outStr = ''
    outStr += f'{len(toWrite)} item were sorted:'

    for i in toWrite:
        outStr += f'\n - {i}'

    getFileName = nameSpace + '.log'
    with open(getFileName, 'w') as f:
        f.write(outStr)
    os.rename(str(getFileName), str(logP / getFileName))
    return str(logP / getFileName)



def mainloop():
    fSorted = []
    filesToSort = [f for f in os.listdir(tDir) if p.Path( tDir / f ).is_file()]
    for fil in filesToSort:
        fP=p.Path(tDir / fil)
        fSuffix = fP.suffix
        fts=fP.stat().st_ctime
        fTS=datetime.datetime.fromtimestamp(fts)
        cT=datetime.datetime.today()
        difT = cT - fTS
        if difT.days>3 or forceCheckFlag:
            if(fSuffix not in suffix):
                suffix.append(fSuffix)
                checkFold()
            try:
                os.rename(str(fP),str(tDir / fSuffix[1:] / fP.parts[-1]))
                fSorted.append(fP.parts[-1])
            except FileExistsError:
                logging.warning(str(fP.parts[-1]) + ' already exists, testing numerals')
                for i in range(1,10):
                    fileN = fP.parts[-1].split('.')
                    fileNIndex = fileN[0] + f'({i}).' +fileN[1]
                    try:
                        os.rename(str(fP),str(tDir / fSuffix[1:] / fileNIndex))
                        fSorted.append(fileNIndex)
                        break
                    except FileExistsError:
                        logging.warning(fileNIndex + ' already exists')
                        if i > 9:
                            logging.critical(str(fP.parts[-1]) + ' could not be sorted, skipped')

    if len(fSorted)>0:
        moveLogFile = writeOutputFiles(fSorted)
        logging.info(f"{len(fSorted)} files were sorted, move specific log file at {moveLogFile}")

# RPyC service definition


def toggle(_input):
    global active


    if isinstance(_input, bool) and active != _input:
        active = _input
        if active:
            logging.info("Download sorter resumed work")
        else:
            logging.info("Download sorter paused using console")
        return("status: " + str(active))
    elif active == _input:
        return ("Status is already set to " + str(active))
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
        logging.info("Download sorter process closed frome console")
        sh = True

    def exposed_triggerCheck(self):
        global forceCheckFlag
        forceCheckFlag=True
        return("Check triggered")




logging.info("Starting rpyc")
# start the rpyc server

server = ThreadedServer(MyService, port = 12345)
th = Thread(target = server.start)
th.daemon = True
th.start()
logging.info("rpyc started")


logging.info("Download sorter initiated")
while True:
    if sh:
        exit()
    runtime+=1
    tToCheck-=1
    if (active and tToCheck<=0) or forceCheckFlag:
        mainloop()
        if forceCheckFlag:
            logging.info("Force check triggered by cmd application")
            forceCheckFlag=False
        cc+=1
        tToCheck=100

    t.sleep(1)


