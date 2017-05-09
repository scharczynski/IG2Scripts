import signal
import time
import importlib
import pytest
from epics import caput, caget, PV, ca, pv, camonitor
import pexpect

def test(proc):
    proc.expect(["ENABLED", pexpect.TIMEOUT, pexpect.EOF], timeout=10)
    
    test = []
    

    for x in range(1,512):
        caput('analog_out_%s' % x, x, wait=True)
        if caget('analog_out_%s' % x) != x:
            test.append(False)
            break
    
    for x in range(1,512):
        caput('digital_out_%s' % x, 1, wait=True)
        if caget('digital_out_%s' % x) != 1:
            test.append(False)
            break
        
    for x in range(1,512):
        caput('int_out_%s' % x, x, wait=True)
        if caget('int_out_%s' % x) != x:
            test.append(False)
            break

    for x in range(1,512):
        caput('string_out_%s' % x, 'string_%s' % x, wait=True)
        if caget('string_out_%s' % x) != 'string_%s' % x:
            test.append(False)
            break

    for x in range(1,512):
        if caget('analog_in_%s' % x) != 0.0:
            test.append(False)
            break

    for x in range(1,512):
        if caget('digital_in_%s' % x) != 0:
            test.append(False)
            break

    for x in range(1,512):
        if caget('int_in_%s' % x) != 0:
            test.append(False)
            break

    for x in range(1,512):
        if caget('string_in_%s' % x) != '':
            test.append(False)
            break

    return all(x == True for x in test)