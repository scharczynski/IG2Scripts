from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time
from util import epics_util as util

def test(proc):

    data = []
    #if lowerlimit is 0, polarity cant change?
    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)
    #print caget('low_limit_1'), caget('low_limit_2'), caget('low_limit_3'), caget('low_limit_4')
    #print caget('high_limit_1'), caget('high_limit_2'), caget('high_limit_3'), caget('high_limit_4')
    while caget('status') not in (0,3):
        time.sleep(1)
        print caget('status')

    util.put_fuzzy('low_limit_1', 0.05, 0.01)
    util.put_fuzzy('low_limit_2', 0.05, 0.01)
    util.put_fuzzy('low_limit_3', 0.05, 0.01)
    util.put_fuzzy('low_limit_4', 0.05, 0.01)

    util.put_check('digital_out_polarity_1', 1)
    util.put_check('digital_out_polarity_2', 1)
    util.put_check('digital_out_polarity_3', 1)
    util.put_check('digital_out_polarity_4', 1)

   

    #print caget('digital_out_polarity_1'), caget('digital_out_polarity_2'), caget('digital_out_polarity_3'), caget('digital_out_polarity_4')
    #print caget('low_limit_1'), caget('low_limit_2'), caget('low_limit_3'), caget('low_limit_4')




    print caget('digital_out_polarity_1'), caget('digital_out_polarity_2'), caget('digital_out_polarity_3'), caget('digital_out_polarity_4')
    print caget('low_limit_1'), caget('low_limit_2'), caget('low_limit_3'), caget('low_limit_4')
    print caget('high_limit_1'), caget('high_limit_2'), caget('high_limit_3'), caget('high_limit_4')

    for i in range(1,5):
        data.append(caget('digital_out_polarity_' + str(i)))


    util.put_check('digital_out_polarity_1', 0)
    util.put_check('digital_out_polarity_2', 0)
    util.put_check('digital_out_polarity_3', 0)
    util.put_check('digital_out_polarity_4', 0)
    
    for i in range(1,5):
        data.append(caget('digital_out_polarity_' + str(i)))

    print caget('digital_out_polarity_1'), caget('digital_out_polarity_2'), caget('digital_out_polarity_3'), caget('digital_out_polarity_4')
    print caget('low_limit_1'), caget('low_limit_2'), caget('low_limit_3'), caget('low_limit_4')
    print caget('high_limit_1'), caget('high_limit_2'), caget('high_limit_3'), caget('high_limit_4')

    #teardown
    util.put_check('digital_out_polarity_1', 1)
    util.put_check('digital_out_polarity_2', 1)
    util.put_check('digital_out_polarity_3', 1)
    util.put_check('digital_out_polarity_4', 1)

    #print caget('digital_out_polarity_1'), caget('digital_out_polarity_2'), caget('digital_out_polarity_3'), caget('digital_out_polarity_4')

    return sum(data)