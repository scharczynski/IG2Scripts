import re
from epics import caget, caput, PV, ca, get_pv, pv
import os
import datetime
import pexpect
import time

def test(proc):

    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

    if connect == 2:

    	caput('trig_buffer', 0)

    	running_state = PV('running_state')
   		paused_state = PV('paused_state')
    	stopped_state = PV('stopped_state')

    print running_state.get == 1

    return -1
