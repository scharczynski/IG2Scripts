from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time
from util import epics_util as util

def test(proc):

    proc.expect(['Announce\(\) success', pexpect.TIMEOUT, pexpect.EOF], timeout=3)

    data = []

    count = PV('in_counts_3')

    util.put_check('trig_mode', 0)
    caput('low_limit_3', 0.0)
    caput('analog_out_period', 10e-4)
    caput('trig_burst', 100)
    caput('trig_buffer', 0)

    def getCount(pvname, value, **kw):
        data.append(value)

    count.add_callback(getCount)

    t0 = time.time()
    while caget('trig_burst') != 100 or caget('low_limit_3') != 0.0 or caget('trig_buffer') != 0.0:
        if time.time() - t0 > 20:
            return "a PV is not being set properly"
        else:
            pass

    caput('initiate', 1)

    t1 = time.time()
    while caget('paused_state') != 1:
        if time.time() - t1 > 30:
            return "pause state never reached"
        else:
            pass

    pass1 = len(data)

    caput('trig_burst', 1000)

    time.sleep(0.1)
    t2 = time.time()
    while caget('trig_burst') != 1000:
        if time.time() - t2 > 20:
            return "trig burst is not being set properly"
        else:
            pass

    caput('initiate', 1)

    t3 = time.time()
    while caget('paused_state') != 1:
        if time.time() - t3 > 30:
            return "pause state never reached 2nd time"
        else:
            pass
    pass2 = len(data) - pass1

    #teardown
    # timeout = time.time()
    # while not (util.put_check('trig_mode', 1)): #and util.put_check('trig_burst', 0)):
    #     if time.time() - timeout > 10:
    #         print "teardown failed"
    #         return False, False
    print util.put_check('trig_burst', 0)
    #util.put_check('trig_mode', 1)
    
    

    return pass1, pass2



