import time
from epics import caput, caget, PV, ca, pv, camonitor, camonitor_clear, poll
import pexpect
from util import epics_util as util



def test(proc):


    proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=10)
    print proc.after

    #util.pv_check('status', 0)
    
    stop = 1001
    data1 = []
    data2 = []

    def getData1(pvname, value, **kw):
        if value != 0:
            data1.append(value)

    def getData2(pvname, value, **kw):
        if value != 0:
            data2.append(value)

    analog1 = PV('analogIn1')
    stop_count = PV('outStopCount')
    init = PV('initiate')
    analog2 = PV('analogIn2')

    analog1.wait_for_connection()
    analog2.wait_for_connection()
    init.wait_for_connection()
    stop_count.wait_for_connection()

    analog1.add_callback(getData1)
    

    

    
    if util.put_check('outStopCount', stop):
        init.put(1)
        t0 = time.time()
        while time.time() -t0 < 30:           
            poll(evt=1.e-5, iot=0.01)
    else:
        print "Stopcount not set"
        return False

    buffered_run = len(data1)
    analog2.add_callback(getData2)

    time.sleep(2)
    if util.put_check('outStopCount', -1):
        init.put(1)
        t0 = time.time()
        while time.time() -t0 < 30:           
            poll(evt=1.e-5, iot=0.01)
    else:
        print "Stopcount not set 2nd time"
        return False

    unbuffered_run = len(data2)

    return buffered_run, unbuffered_run
