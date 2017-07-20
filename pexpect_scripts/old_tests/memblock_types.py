import time
from epics import caput, caget, PV, ca, pv, camonitor
import pexpect
from util import epics_util as util

def test(proc):
    proc.expect(["ENABLED", pexpect.TIMEOUT, pexpect.EOF], timeout=10)
    
    test = []
    

    for x in range(1,512):
        test.append(util.put_check('analog_out_'+str(x), x))

    for x in range(1,512):
        test.append(util.put_check('digital_out_' + str(x), 1))

    for x in range(1,512):
        test.append(util.put_check('int_out_' + str(x), x))

    for x in range(1,512): 
        test.append(util.put_check('string_out_' + str(x), str(x)))

    for x in range(1,512):
        test.append(util.pv_check('analog_in_' + str(x), 0))

    for x in range(1,512):
        test.append(util.pv_check('digital_in_' + str(x), 0))

    for x in range(1,512):
        test.append(util.pv_check('int_in_' + str(x), 0))

    for x in range(1,512):
        test.append(util.pv_check('string_in_' + str(x), ''))

    if all(x == True for x in test):
        return True
    else:
        print test
        return False
