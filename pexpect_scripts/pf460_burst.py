from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time
from util import epics_util as util

def test(proc):

    data = []
    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

    util.put_check('acquisition_mode', 1)
    util.put_check('buffered_acquisition', 0)
    util.put_check('burst_count', 100)

    return caget('burst_count')
