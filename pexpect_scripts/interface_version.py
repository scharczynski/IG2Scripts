import time
from epics import caput, caget, __version__
import pexpect

def test(proc): 

    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'EPICS ENVIRONMENT 2_6_7 ENABLED'
], timeout=5)

    return proc.after



