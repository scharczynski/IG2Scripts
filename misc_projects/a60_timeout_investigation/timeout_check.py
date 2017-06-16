from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time
import random

proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/reconnect.xml")
f = open('log.txt', 'w')
iterations = 0
failures = 0
while True:

    connection = proc.expect(['Announce\(\) success','Error connecting to host','Announce: RPC: Timed out', 'Announce\(\) fail', 'Device.*in error', pexpect.TIMEOUT, pexpect.EOF], timeout=3)

    if connection in (1,2,3,4):
        print "connection timeout detected"
        print proc.before
        print "&*&&&&&&&&&"
        print proc.after
        failures += 1
    

    dum1 = caget('analogIn1')
    dum2 = caget('analogIn2')

    caput('analogOut1', random.random())
    caput('analogOut2', random.random())


    f.write(str(connection))
    f.write("\n")
    f.write(str(proc.after))
    f.write("\n")
    f.write(str(proc.before))
    f.write("\n")
    f.write("failures: " + str(failures))
    f.write("\n")
    f.write("iterations :" + str(iterations))
    f.write("\n")
    f.write("----------------------------------------------------------")
    f.write("\n")
    f.flush()
    iterations += 1
    time.sleep(10)


