from epics import caget, caput, PV, ca, get_pv, pv, camonitor, poll
import pexpect
import time
from util import epics_util as util

def test(proc):

    data = []
    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

    util.put_check('acquisition_mode', 1)
    util.put_check('buffered_acquisition', 1)
    util.put_check('stop_count', 1000)
    #util.put_check('range_1', 0)

    current1 = PV('current_in_1')

    def getCount(pvname, value, **kw):
        data.append(value)

    current1.add_callback(getCount)

    caput('initiate', 1)

    t0 = time.time()
    while time.time() - t0 < 30 and len(data) < 500:
        poll(evt=1.e-5, iot=0.01)
    
    caput('initiate', 0)
    print len(data)
    time.sleep(0.5)
    print len(data)
    time.sleep(5)

    return len(data)
    



    





