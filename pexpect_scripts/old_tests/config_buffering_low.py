from epics import caget, caput, PV, ca, get_pv, pv, poll
import pexpect
import time
from util import epics_util as util

def test(proc):
    connect = proc.expect(['Announce\(\) success', pexpect.TIMEOUT, pexpect.EOF], timeout=3)

    count3 = PV('in_counts_3')


    data3 = []

          
    def getCount3(pvname, value, **kw):
        data3.append(value)

    
    if util.put_check('low_limit_3', 0.0) and util.put_check('low_limit_4', 0.0) and util.put_check('trig_buffer', 1000) and util.put_fuzzy('analog_out_period', 10e-5, 0.05):
        pass
    else:
        print "setting not taking place"
        return False, False


    


    count3.add_callback(getCount3)
    caput('initiate', 1)
    t0 = time.time()
    while time.time() -t0 < 3:
        
        poll(evt=1.e-5, iot=0.01)
       


    time.sleep(2)
    
    return len(data3)
