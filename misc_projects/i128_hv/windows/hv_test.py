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
    proc = subprocess.Popen("C:\\Users\\steve\\workspace\\windowscopy\\ig2-2_6_7\\service\\ig2-2.6.7.exe config\\testsetup.xml",
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    nbsr = NBSR(proc.stdout)
    #on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
    subprocess.call('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
    time.sleep(2)

    while "success: A1" not in str(nbsr.readline(0.1)):
        time.sleep(1)

    line = nbsr.readline(0.1)
    t0 = time.time()

    hv = 650

    while (time.time() - t0) < 60:
        if ("High voltage not available" in str(line)) or ("Invalid high voltage" in str(line)):
            m = re.search(
                '(High voltage not available|Invalid high voltage)', line)
            kill(proc)
            return m.group() + " TIME: " + str(time.time()- start_time)
        if caget('hv_command') != hv:
            caput('hv_command', hv)
            line = nbsr.readline(1)

        time.sleep(1)

    sys.stdout.flush()
    kill(proc)
    return "no errors TIME: " + str(time.time() - start_time)


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

    time.sleep(60)
