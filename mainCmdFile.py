from time import sleep
import rpyc
import sys 
try:
    conn = rpyc.connect("localhost", 12345)
except:
    print("Main program is not running, console will be aborted")
    sleep(5)
    sys.exit()
c = conn.root

cRT=0
print("Conection made\n")
print('init console, type "help" for info about commands')
while True:
    # tmpRT=c.runtime()
    # if tmpRT != cRT:
    #     cRT = tmpRT
    #     print(cRT)
    # sleep(5)
    _in = input(">").lower().split(" ")
    if(_in[0] == "help"):
        print(" rt --> print main loop runtime \n help --> print this menu \n status --> (no args = return status, bool var = Set status \n closemain --> close the main program and this curent program \n close --> close this program\n triggcheck --> triggers main app to sort all files regardless of time since creation" )
    
    
    elif _in[0] == "rt":
        print(c.runtime())


    elif _in[0] == "status":
        if len(_in) == 2:
            tmparg = _in[1]
            if tmparg == "true" or tmparg == "false":
                print(c.toggleRun(tmparg))
                # print("Main loop set to " + tmparg)
            else:
                print(tmparg + " is not an suported variable")
        else:
            print("\nFetching status of mainloop")
            print(c.toggleRun("pass"))
    
    
    elif _in[0] == "closemain":
        c.close()
        print("Main closed, this script will be closed")
        sleep(5)
        sys.exit()


    elif _in[0] == "close":
        print("This script will be closed")
        sleep(5)
        sys.exit()
    
    elif _in[0] == "triggercheck":
        print(c.triggerCheck())


    else:
        print("unknown cmd, check help")






