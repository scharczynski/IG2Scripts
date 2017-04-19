import time
import subprocess
import sys
import re
from epics import caget, caput
from nbstreamreader import NonBlockingStreamReader as NBSR

data = []
file = open('log2.txt', 'w')
on = subprocess.Popen('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
start_time = time.time()

def test():
    proc = subprocess.Popen("C:\\Users\\steve\\workspace\\windowscopy\\ig2-2_6_7\\service\\ig2-2.6.7.exe config\\a560.xml",
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    nbsr = NBSR(proc.stdout)
    #on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
    subprocess.call('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
    time.sleep(2)

    line = nbsr.readline(0.1)
    t0 = time.time()

    while (time.time() - t0) < 60:
        if "success: A1" in str(line):
            proc.kill()
            print "connected to a560"
            return 1
        else:
            line = nbsr.readline(0.5)

    sys.stdout.flush()
    kill(proc)
    print "never connected, final line is " + str(line) +"time is: " + str(time.time() - start_time)
    return 0


def kill(proc):
    while proc.poll() is None:
        proc.kill()


success_rate = 0
good_trials = 0
trials = 0

while True:
    output = test()
    data.append(output)
    #print data
    print output
    time.sleep(1)
    file.write(str(output))
    file.write("\n")
    subprocess.call('curl "http://admin:1234@192.168.100.36/outlet?1=OFF"')

    if output == 1:
        good_trials += 1
    trials += 1

    success_rate = 100.00 * (good_trials/trials)

    print "success rate is: " + str(success_rate) + "%, there have been " + str(trials - good_trials) + " failures out of " + str(trials) + " trials    "

    time.sleep(30)
