import re
import epics
import os
import signal
import time
import importlib
import pytest
from epics import caput, caget, PV, ca, pv, camonitor
import pexpect

def test(proc):
    #time.sleep(2)
    proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=0.25)
    caget('c_test1')
    caget("c_test2")
    t1 = PV('c_test1')
    t2 = PV('c_test2')
    camonitor('c_test1')
    camonitor('c_test2')
    #print t2.get()
    t1.put(1, wait=True)
    time.sleep(0.25)
    t2.put(45, wait=True)
    time.sleep(0.25)
    #print t2.get()

    print t2.info
    return(caget('c_test1'), caget('c_test2'))
