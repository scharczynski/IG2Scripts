from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time

def test(proc):

    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

    caput('initiate', 1)

    time.sleep(2)

    return caget('analog_in_1'), caget('analog_in_2'), caget('current_in_1'), caget('current_in_2'), caget('current_in_3'),
         caget('current_in_4'), caget('channel_in_1'), caget('channel_in_2'), caget('channel_in_3'), caget('channel_in_4')