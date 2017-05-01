import re
from epics import caget, caput, PV, ca, get_pv, pv
import os
import datetime
import pexpect
import time

def test(proc):
    proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=3)
    #print proc.before
    #print proc.after
    di1 = caget('digitalIn1')
    di2 = caget('digitalIn2')
    di3 = caget('digitalIn3')
    di4 = caget('digitalIn4')
    ai1 = caget('analogIn1')
    ai2 = caget('analogIn2')

    caput('digitalOut1', 1)
    caput('digitalOut2', 1)
    caput('digitalOut3', 1)
    caput('digitalOut4', 1)

    time.sleep(1)

    do1 = caget('digitalOut1')
    do2 = caget('digitalOut2')
    do3 = caget('digitalOut3')
    do4 = caget('digitalOut4')

    caput('analogOut1', 5)
    caput('analogOut2', 9)

    time.sleep(1)

    ao1 = caget('analogOut1')
    ao2 = caget('analogOut2')

    return (do1, do2, do3, do4, ao1, ao2)
