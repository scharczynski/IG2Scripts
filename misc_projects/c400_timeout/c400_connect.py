import time
import subprocess
import sys
import re
import os

from nbstreamreader import NonBlockingStreamReader as NBSR


data = []
f = open('c400log2.txt', 'w')
#subprocess.call(
#    'curl --max-time 30 "http://admin:1234@192.168.100.36/outlet?1=CCL"')
start_time = time.time()


def test():
    proc = subprocess.Popen("C:\\Users\\steve\\workspace\\windowscopy\\ig2-2_6_7\\service\\ig2-2.6.7.exe config\\c400.xml",
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    nbsr = NBSR(proc.stdout)

    line = nbsr.readline(0.1)
    t0 = time.time()

    while (time.time() - t0) < 30:
        print "**** " + str(line)
        if "success: C1" in str(line):
            print "connected to c400"
            while time.time() - t0 < 30:
                print str(line)
                if "Error connecting to host" in str(line) or "RPC: Timed out" in str(line):
                    print line
                    proc.kill()
                    return 0
                else:
                    line = nbsr.readline(0.1)
            proc.kill()
            return 1
        else:
            line = nbsr.readline(0.5)

    sys.stdout.flush()

    print "never connected, final line is " + str(line) + "time is: " + str(time.time() - start_time)

    proc.kill()
    return -1


def kill(proc):
    while proc.poll() is None:
        proc.kill()


success_rate = 0
good_trials = 0
trials = 0
timed_out = 0
no_connects = 0



while True:
    output = test()
    data.append(output)
    # print data
    print output
    time.sleep(1)
    f.write(str(output))
    f.write("\n")
    f.flush()

    if output == 1:
        good_trials += 1
    elif output == -1:
        no_connects += 1
    else:
        timed_out += 1

    

    print "successful connections: " + str(good_trials) + " timed out connections: " + str(timed_out) + " never connected: " + str(no_connects)

    time.sleep(10)
