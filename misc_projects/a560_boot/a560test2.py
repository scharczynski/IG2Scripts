import time
import subprocess
import sys
import re
from epics import caget, caput

data = []
file = open('log.txt', 'w')
on = subprocess.Popen('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
start_time = time.time()

def test():
    proc = subprocess.Popen("C:\\Users\\steve\\workspace\\windowscopy\\ig2-2_6_7\\service\\ig2-2.6.7.exe config\\a560.xml",
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    
    #on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
    subprocess.call('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
    time.sleep(2)

    t0 = time.time()

    while (time.time() - t0) < 60:
        if caget("device_state") == 0:
            proc.kill()
            return "connected to a560"
        else:
            time.sleep(0.5)

    sys.stdout.flush()
    kill(proc)
    return "never connected, device state is " + caget('device_state') +"time is: " + str(time.time() - start_time)


def kill(proc):
    while proc.poll() is None:
        proc.kill()


while True:
    output = test()
    data.append(output)
    #print data
    print output
    time.sleep(1)
    file.write(str(output))
    file.write("\n")
    subprocess.call('curl "http://admin:1234@192.168.100.36/outlet?1=OFF"')

    time.sleep(30)
