from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time

def test(proc):

    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

    
    #caput('low_limit_3', 1.0)
    #caput('low_limit_4', 1.0)
    caput('trig_buffer', 100)
    caput('analog_out_period', 10e-4)

    count3 = PV('in_counts_3')
    count4 = PV('in_counts_4')
    limit3 = PV('low_limit_3')
    limit4 = PV('low_limit_4')

    limit3.put(1.0)
    limit4.put(1.0)

    setting = proc.expect([pexpect.TIMEOUT, 'Error setting C400'])
    if setting == 1:
        print "a setting is preventing limits from being set"
        caput('digital_out_polarity_3', 1)
        caput('digital_out_polarity_4', 1)

    data = []
    data2 = []

    while limit3.value == 0.0 or limit4.value == 0.0:
        print "waiting for limits"
        

    caput('initiate', 1)

    for i in range (1,100):
        data.append(count3.value)
        data2.append(count4.value)
        time.sleep(0.01)

    caput('low_limit_3', 0.0)
    time.sleep(1)
    caput('initiate', 1)

    for i in range (1,100):
        data.append(count3.value)
        data2.append(count4.value)
        time.sleep(0.01)

    return sum(data), sum(data2)