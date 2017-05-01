import re
from epics import caget, caput, PV, ca, get_pv, pv
import os
import datetime
import pexpect
import time

def test(proc):

    proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=3)

    running_state = caget('running_state')
    paused_state = caget('paused_state')
    stopped_state = caget('stopped_state')

    print running_state, paused_state, stopped_state

    return (do1, do2, do3, do4, ao1, ao2)
