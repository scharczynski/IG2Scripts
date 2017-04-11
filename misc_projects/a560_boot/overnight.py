from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import datetime
import pexpect
import time

data=[]
file = open('log2.txt', 'w')
pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')
pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?2=ON"')
proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 config/overnight_test.xml")

def test():

    on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=ON"')

    output = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'])

    if output == 2:
        cycle = pexpect.spawn('curl "http://admin:1234@192.168.100.36/script?run002=run"')
    else:
        print proc.after
        print proc.before
        return "failed"

    output = proc.expect(['Announce: RPC: Timed out', 'Announce\(\) fail', 'Device.*in error', pexpect.TIMEOUT], timeout=30)
    print proc.before
    print proc.after
    if output == 0 or output == 1 or output == 2:
        cycle = pexpect.spawn('curl "http://admin:1234@192.168.100.36/script?run005=run"')
    else:
        print proc.after
        print proc.before
        return "disconnected strangely"
    output = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=45)

    if output == 2:
        print "we did it"
        return proc.after
    else:
        print proc.before, proc.after
        return proc.after



while True:
    output = test()
    data.append(output)
    print data
    print output
    time.sleep(1)
    file.write(str(output))
    file.write("\n")
    reset = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=OFF"')
    time.sleep(10)  