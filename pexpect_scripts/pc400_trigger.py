from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time

def test(proc):

    data = []







    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)
    #caput('trig_mode', 1)
    print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')

    
    caput('trig_source_start', 0)
    caput('trig_source_pause', 0)
    caput('trig_source_stop', 0)
    caput('trig_mode', 0)

    print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')
    while (caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')) != (0,0,0,0):
        print "waiting"

    for i in range(0,4):
        caput('trig_source_start', i)
        time.sleep(0.1)
        if caget('trig_source_start') != i:
            print str(i) + ":iFasle"
            print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')   
            data.append(False)
        else:
            data.append(True)
            
        #print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop') 
        for j in range(0,4):
            caput('trig_source_pause', j)
            time.sleep(0.1)

            if caget('trig_source_pause') != j:
                print str(j) + ":jFasle"
                print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')   
                data.append(False)
            else:
                data.append(True)

            #print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')       
            for k in range(0,4):
                caput('trig_source_stop', k)
                time.sleep(0.1)

                if k == j and j != 0:
                    bad = proc.expect([pexpect.TIMEOUT,"Error setting C400 configuration"])
                    if bad == 1:
                        data.append(True) 
                elif caget('trig_source_stop') != k:
                    print str(k) + ":kFasle"
                    print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')   
                    data.append(False)
                else:
                    data.append(True)

                #print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')                  
            caput('trig_source_stop', 0)      
        caput('trig_source_pause', 0)

    
    for i in range(0,7):
        print i
        caput('trig_mode', i)
        time.sleep(1)
        if caget('trig_mode') != i:
            data.append(True)
        print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')

    print data

    return all(x == True for x in data)

    

   