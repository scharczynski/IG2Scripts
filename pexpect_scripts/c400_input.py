from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time

def test(proc):

    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)
    
    time.sleep(1)


    caput('low_limit_1', 0.0)
    caput('low_limit_2', 0.0)
    caput('low_limit_3', 0.0)
    caput('low_limit_4', 0.0)

    count1, count2, count3, count4 = PV('in_counts_1'), PV('in_counts_2'), PV('in_counts_3'), PV('in_counts_4')

    rate1, rate2, rate3, rate4 = PV('analog_in_rate_1'), PV('analog_in_rate_2'), PV('analog_in_rate_3'), PV('analog_in_rate_4')

    bias1, bias2, bias3, bias4 = PV('analog_in_bias_1'), PV('analog_in_bias_2'), PV('analog_in_bias_3'), PV('analog_in_bias_4')



    caput('initiate', 1)

    time.sleep(5)


    
    




    caput('analog_out_bias_1', 100)
    caput('analog_out_bias_2', 200)
    caput('analog_out_bias_3', 300)
    caput('analog_out_bias_4', 400)


    time.sleep(2)

    
    counts = [count1.value, count2.value, count3.value, count4.value]
    rates = [rate1.value, rate2.value, rate3.value, rate4.value]
    biases = [bias1.value, bias2.value, bias3.value, bias4.value]

    return all(x != None for x in (counts + rates + biases))