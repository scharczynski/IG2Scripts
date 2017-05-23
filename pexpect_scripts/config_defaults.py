import re
from epics import caget, caput, PV, ca, get_pv, pv
import os
import datetime
import pexpect


def test(proc):
    proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=3)
    a,b,c = caget('testA'), caget('testB'), caget('testC')
    return (a,b,c)
