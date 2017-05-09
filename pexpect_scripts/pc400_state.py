import re
from epics import caget, caput, PV, ca, get_pv, pv
import os
import datetime
import pexpect
import time

def test(proc):

    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

    data = []

    running_state = PV('running_state')
    paused_state = PV('paused_state')
    stopped_state = PV('stopped_state')

    if connect == 2:
        caput('trig_buffer', 0)
        
    data.append ((running_state.value, paused_state.value, stopped_state.value) == (0,0,0))


    caput('trig_burst', 100)
    caput('initiate', 1)
    time.sleep(2)
    data.append ((running_state.value, paused_state.value, stopped_state.value) == (0,1,0))

    caput('trig_burst', 0)
    caput('initiate', 1)

    time.sleep(1)

    data.append ((running_state.value, paused_state.value, stopped_state.value) == (1,0,0))

    caput('initiate', 0)
    
    time.sleep(1)

    data.append ((running_state.value, paused_state.value, stopped_state.value) == (0,0,1))

    return all(x == True for x in data)
