from epics import caget, caput, PV, ca, get_pv, pv, camonitor, poll
import pexpect
import time
from util import epics_util as util

def test(proc):

    data = []
    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

    time.sleep(1)

    util.put_check('acquisition_mode', 1)
    util.put_check('buffered_acquisition', 0)
    util.put_check('stop_count', 0)

    current1 = PV('current_in_1')

    def getCount(pvname, value, **kw):
        data.append(value)


    current1.add_callback(getCount)

    caput('initiate', 1)

    t0 = time.time()
    while time.time() -t0 < 10:
        if len(data2) >= 3000:
            caput('initiate', 0)
            break
        poll(evt=1.e-5, iot=0.01)

    #caput('initiate', 0)

    # util.put_check('buffered_acquisition', 0)
    # util.put_check('stop_count', 0)
    # #print current1.callbacks
    # current1.remove_callback(1)
    # current1.add_callback(getCount2)

    # caput('initiate', 1)

    # t1 = time.time()
    # while time.time() -t1 < 10:
    #     if len(data2) >= 500:
    #         caput('initiate', 0)
    #         break
    #     poll(evt=1.e-5, iot=0.01)
    

    time.sleep(1)


    return len(data)    
    



    





