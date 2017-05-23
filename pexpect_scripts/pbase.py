import time
import importlib
from epics import caput, caget, PV, ca, pv, camonitor
import pexpect

def test(proc):
    proc.expect(["ENABLED", pexpect.TIMEOUT, pexpect.EOF], timeout=10)
    caget('c_test1')
    caget("c_test2")
    t1 = PV('c_test1')
    t2 = PV('c_test2')
    camonitor('c_test1')
    camonitor('c_test2')
    t1.put(1, wait=True)
    time.sleep(0.25)
    t2.put(45, wait=True)
    time.sleep(0.25)

    return(caget('c_test1'), caget('c_test2'))
