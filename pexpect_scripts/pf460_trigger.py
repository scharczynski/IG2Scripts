from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time
from util import epics_util as util

def test(proc):

    data = []
    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)
    #caput('acquisition_mode', 1)
    print caget('acquisition_mode'), caget('start_trigger_source'), caget('pause_trigger_source'), caget('stop_trigger_source')

    
    caput('start_trigger_source', 0)
    caput('pause_trigger_source', 0)
    caput('stop_trigger_source', 0)
    caput('acquisition_mode', 0)

    util.pv_check('start_trigger_source', 0)
    util.pv_check('pause_trigger_source', 0)
    util.pv_check('stop_trigger_source', 0)
    util.pv_check('acquisition_mode', 0)

   # while (caget('acquisition_mode'), caget('start_trigger_source'), caget('pause_trigger_source'), caget('stop_trigger_source')) != (0,0,0,0):
    #    print "waiting"

    for i in range(0,2):
        caput('start_trigger_source', i)
        time.sleep(0.1)
        if caget('start_trigger_source') != i:
            data.append(False)
        else:
            data.append(True)
            
        for j in range(0,2):
            caput('pause_trigger_source', j)
            time.sleep(0.1)

            if caget('pause_trigger_source') != j:
                data.append(False)
            else:
                data.append(True)

            #print caget('acquisition_mode'), caget('start_trigger_source'), caget('pause_trigger_source'), caget('stop_trigger_source')       
            for k in range(0,2):
                caput('stop_trigger_source', k)
                time.sleep(0.1)

                if k == j and j != 0:
                    bad = proc.expect([pexpect.TIMEOUT,"Error setting C400 configuration"])
                    if bad == 1:
                        data.append(True) 
                elif caget('stop_trigger_source') != k:
                    #print str(k) + ":kFasle"
                    #print caget('acquisition_mode'), caget('start_trigger_source'), caget('pause_trigger_source'), caget('stop_trigger_source')   
                    data.append(False)
                else:
                    data.append(True)
             
            caput('stop_trigger_source', 0)      
        caput('pause_trigger_source', 0)

    
    for i in range(0,6):
        caput('acquisition_mode', i)
        time.sleep(1)
        if caget('acquisition_mode') != i:
            data.append(False)
        else: 
            data.append(True)

    for i in range(0,2):
        data.append(util.put_check('bnc_start_gate', i))

    for i in range(0, 4):
        data.append(util.put_check('range_1', i))
        data.append(util.put_check('range_2', i))
        data.append(util.put_check('range_3', i))
        data.append(util.put_check('range_4', i))

    ##teardown

    util.put_check('acquisition_mode', 1)

    return all(x == True for x in data)

    

   