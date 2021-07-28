from time import sleep

import rpyc
conn = rpyc.connect("localhost", 12345)
c = conn.root
cRT=0
print('int console, type "help" for info about commands')
while True:
    # tmpRT=c.runtime()
    # if tmpRT != cRT:
    #     cRT = tmpRT
    #     print(cRT)
    # sleep(5)
    _in = input(">").split(" ")
    if(_in[0] == "help"):
        print("rt --> print main loop rT \nhelp --> print this menu \nstatus (no args = return status, bool var = Set status")
    elif _in[0] == "rt":
        print(c.runtime()[0])
    elif _in[0] == "status":
        if len(_in) == 2:
            tmparg = _in[1]
            if tmparg == "True" or tmparg == "False":
                print(c.toggleRun(tmparg))
                # print("Main loop set to " + tmparg)
            else:
                print(tmparg + " is not an suported variable")
        else:
            print("\nFetching status of mainloop")
            print(c.toggleRun("pass"))
    elif _in[0] == "closeMain":
        c.close()







