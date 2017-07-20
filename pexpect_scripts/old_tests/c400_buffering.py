from epics import caget, caput, PV, ca, get_pv, pv, poll
import pexpect
import time
from util import epics_util as util

def test(proc):
    connect = proc.expect(['Announce\(\) success', pexpect.TIMEOUT, pexpect.EOF], timeout=3)

    count3 = PV('in_counts_3')
    count4 = PV('in_counts_4')

    data1 = []
    data2 = []

          
    def getCount1(pvname, value, **kw):
        data1.append(value)

    def getCount2(pvname, value, **kw):
        data2.append(value)

   
    

   
    if util.put_check('low_limit_3', 0.0) and util.put_check('low_limit_4', 0.0) and util.put_check('trig_buffer', 1000) and util.put_fuzzy('analog_out_period', 10e-5, 0.05):
        pass
    else:
        print "setting not taking place"
        return False, False



   

    time.sleep(1)
    count3.add_callback(getCount1)
    caput('initiate', 1)
    t0 = time.time()
    while time.time() -t0 < 3:
        
        poll(evt=1.e-5, iot=0.01)
       
    run1 = len(data1)
    count3.remove_callback(1)
    count3.add_callback(getCount2)
    if util.put_check('trig_buffer', 500):
        pass
    else:
        print "setting 2nd time not taking place"
        return False, False
    caput('initiate', 1)
    t1 = time.time()
    while time.time() -t1 < 3:   
        poll(evt=1.e-5, iot=0.01)
    #time.sleep(2)

    run2 = len(data2)

    return run1, run2
