import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll
import time
from util import epics_util as util
from tests.Tester import Tester


class C400_Tester(Tester):

    def __init__(self, path, test_name):
        Tester.__init__(self, path)
        self.path += str(test_name) + ".xml"
        self.proc = pexpect.spawn(self.path)

    def accumulate_mode(self):
        data = []

        connect = proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

        count = PV('in_counts_3')

        caput('low_limit_3', 0.0)
        caput('trig_buffer', 1000)
        caput('analog_out_period', 10e-5)

        def getCount(pvname, value, **kw):
            data.append(value)

        count.add_callback(getCount)

        time.sleep(1)

        def run(mode):

            caput('accum_mode', mode)
            time.sleep(1)

            t0 = time.time()
            while caget('accum_mode') != mode or caget('low_limit_3') != 0.0:
                if time.time() - t0 > 20:
                    print "accum mode or low limit not being set"
                    break

            caput('initiate', 1)
            time.sleep(5)
            caput('initiate', 0)

        run(0)
        if len(data) > 10:
            non_accum = data[-1] - data[-6]
        else:
            return "didnt get data"
        run(1)
        if len(data) > 10:
            accum = data[-1] - data[-6]
        else:
            return "didnt get data "

        # teardown
        while caget('accum_mode') != 0:
            caput('accum_mode', 0)
        return non_accum, accum, data[0]

    def buffering(self):
        connect = proc.expect(
            ['Announce\(\) success', pexpect.TIMEOUT, pexpect.EOF], timeout=3)

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
        while time.time() - t0 < 3:

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
        while time.time() - t1 < 3:
            poll(evt=1.e-5, iot=0.01)

        run2 = len(data2)

        return run1, run2

    def burst_size(self):
        proc.expect(['Announce\(\) success',
                     pexpect.TIMEOUT, pexpect.EOF], timeout=3)

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

        # teardown

        util.put_check('trig_burst', 0)

        return pass1, pass2

    def io(self):
        connect = proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

        time.sleep(1)

        caput('low_limit_1', 0.0)
        caput('low_limit_2', 0.0)
        caput('low_limit_3', 0.0)
        caput('low_limit_4', 0.0)

        count1, count2, count3, count4 = PV('in_counts_1'), PV(
            'in_counts_2'), PV('in_counts_3'), PV('in_counts_4')

        rate1, rate2, rate3, rate4 = PV('analog_in_rate_1'), PV(
            'analog_in_rate_2'), PV('analog_in_rate_3'), PV('analog_in_rate_4')

        bias1, bias2, bias3, bias4 = PV('analog_in_bias_1'), PV(
            'analog_in_bias_2'), PV('analog_in_bias_3'), PV('analog_in_bias_4')

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

    def integration_set(self):
        data = []
        connect = proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

        count = PV('in_counts_3')

        caput('trig_mode', 1)
        caput('low_limit_3', 0.0)
        caput('low_limit_4', 0.0)
        caput('trig_buffer', 1000)
        caput('analog_out_period', 10e-5)

        def getCount(pvname, value, **kw):
            data.append(value)

        count.add_callback(getCount)

        t0 = time.time()
        while caget('low_limit_3') != 0.0 or caget('low_limit_3') != 0.0 or caget('analog_out_period') != 10e-5:
            if time.time() - t0 > 20:
                return "some pv is not being set"
            else:
                pass

        caput('initiate', 1)
        time.sleep(2)

        fast = count.value

        caput('analog_out_period', 10e-3)

        t1 = time.time()
        while caget('analog_out_period') != 10e-3:
            if time.time() - t1 > 20:
                return "integration period is not being set"
            else:
                pass

        caput('initiate', 1)
        time.sleep(5)

        slow = count.value

        return slow / (fast + 0.01 * fast), slow / (fast - 0.01 * fast)

    def discriminator_limits(self):
        data = []
        connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

        count = PV('in_counts_3')

        caput('trig_mode', 1)
        caput('low_limit_3', 0.0)
        caput('low_limit_4', 0.0)
        caput('trig_buffer', 1000)
        caput('analog_out_period', 10e-5)


        def getCount(pvname, value, **kw):
            data.append(value)


        count.add_callback(getCount)

        t0 = time.time()
        while caget('low_limit_3') != 0.0 or caget('low_limit_3') != 0.0 or caget('analog_out_period') != 10e-5:
            if time.time() - t0 > 20:
                return "some pv is not being set"
            else:
                pass


        caput('initiate', 1)
        time.sleep(2)

        fast = count.value

        caput('analog_out_period', 10e-3)

        t1 = time.time()
        while caget('analog_out_period') != 10e-3:
            if time.time() - t1 > 20:
                return "integration period is not being set"
            else:
                pass

        caput('initiate', 1)
        time.sleep(5)

        slow = count.value
        
        return slow/(fast + 0.01*fast), slow/(fast - 0.01*fast)
    
    def polarity(self):

        data = []
        #if lowerlimit is 0, polarity cant change?
        connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)
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


        for i in range(1,5):
            data.append(caget('digital_out_polarity_' + str(i)))

        util.put_check('digital_out_polarity_1', 0)
        util.put_check('digital_out_polarity_2', 0)
        util.put_check('digital_out_polarity_3', 0)
        util.put_check('digital_out_polarity_4', 0)
        
        for i in range(1,5):
            data.append(caget('digital_out_polarity_' + str(i)))

        # print caget('digital_out_polarity_1'), caget('digital_out_polarity_2'), caget('digital_out_polarity_3'), caget('digital_out_polarity_4')
        # print caget('low_limit_1'), caget('low_limit_2'), caget('low_limit_3'), caget('low_limit_4')
        # print caget('high_limit_1'), caget('high_limit_2'), caget('high_limit_3'), caget('high_limit_4')

        #teardown
        util.put_check('digital_out_polarity_1', 1)
        util.put_check('digital_out_polarity_2', 1)
        util.put_check('digital_out_polarity_3', 1)
        util.put_check('digital_out_polarity_4', 1)

        return sum(data)
    
    def pulse