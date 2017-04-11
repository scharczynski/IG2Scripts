import subprocess
import re
from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import os
import datetime
import pexpect
import time


def test(proc):
    #print proc.pid
    #print ca.current_context()
    #t1 = PV('c_test1')
    #t2 = PV('c_test2')
    #print pv._PVcache_
    proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=0.25)
    t1 = PV('wire1')
    #print t1.info
    t2 = PV('wire2')
    camonitor('wire1')
    camonitor('wire2')
    #t1.connect()
    #t2.connect()
    t1.put(65, wait=True)
    time.sleep(0.25)
    #print t1.info
    #print t2.info

    #print pv._PVcache_

    return(caget('wire1'), caget('wire2'))
