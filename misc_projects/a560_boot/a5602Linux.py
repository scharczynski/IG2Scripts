import time
import subprocess
import sys
import re
import os
import pexpect
from epics import caget, caput

data = []
f = open('log.txt', 'w')
on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
start_time = time.time()


def connect(timeout):
    t0 = time.time()

    while (time.time() - t0) < timeout:
        state = caget("device_state")
         if state == 0:
            proc.kill()
            print "connected to a560"
            return 1
        else:
            print state
            time.sleep(0.5)

    return 0

def test():
    proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 config/a560test2.xml")
    
    
    cycle = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')

    time.sleep(2)

    sys.stdout.flush()
    kill(proc)

    if connect(60) == 1:
        return 1
    
    time.sleep(5)

    if connect(60) == 1:
        return 1
    else: 
        print "never connected, device state is " + caget('device_state') +"time is: " + str(time.time() - start_time)
        return 0

def kill(proc):
    while proc.poll() is None:
        proc.kill()


while True:
    output = test()
    data.append(output)

    print output
    time.sleep(1)
    f.write(str(output))
    f.write("\n")
    f.flush()
    os.fsync()
    cycle = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=OFF"')

    if output == 1:
        good_trials += 1
    trials += 1

    success_rate = 100.00 * float(good_trials) / trials

    print "success rate is: " + str(success_rate) + "%, there have been " + str(trials - good_trials) + " failures out of " + str(trials) + " trials    "

    time.sleep(5)


