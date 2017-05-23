import subprocess
import re
from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import os
import datetime
import pexpect
import time


def test(proc):
    proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=0.25)

    t1 = PV('wire1')
    t2 = PV('wire2')

    camonitor('wire1')
    camonitor('wire2')

    t1.put(65, wait=True)
    time.sleep(1)


    return(caget('wire1'), caget('wire2'))
