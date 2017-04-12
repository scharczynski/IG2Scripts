from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import datetime
import pexpect
import time
import os

data=[]
file = open('log2.txt', 'w')


def test():

    on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
    time.sleep(20)
    return ping()

 
def ping():
    pinger = os.system('ping -c 3 192.168.100.73' )
    #result = p([pexpect.TIMEOUT, pexpect.EOF, 'Destination Host Unreachable', 'time='])
    if pinger == 0:
        return True
    else:
        return False
loop = True
while loop:
    output = test()
    data.append(output)
    print data
    time.sleep(1)
    file.write(str(output))
    file.write("\n")
    if output == False:
        print "ping failed, exiting"
        break
    print "sanity check"
    reset = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=OFF"')
    time.sleep(60)  