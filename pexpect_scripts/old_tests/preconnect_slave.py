from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import datetime
import pexpect
import time

def test(proc):
    output = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'])

    if output == 2:
        cycle = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?2=OFF"')

    else:
        print "device appears to not be connected"
        return False

    output = proc.expect(['Announce: RPC: Timed out', 'Announce\(\) fail', 'Device.*in error', pexpect.TIMEOUT], timeout=10)

    if output == 0 or 1:
        cycle = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?2=ON"')
    else:
        print "device time out not detected"
        return False
    output = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=10)

    if output == 2:
        print "we did it"
        return True
    else:
        print proc.before, proc.after
        print "device did not reconnect"
        return False
