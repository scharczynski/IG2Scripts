from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time

def test(proc):
    #cycle = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?3=CCL"')

    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=10)



    running_state = PV('running_state')
    paused_state = PV('paused_state')
    stopped_state = PV('stopped_state')



    return [running_state.value, paused_state.value, stopped_state.value]
