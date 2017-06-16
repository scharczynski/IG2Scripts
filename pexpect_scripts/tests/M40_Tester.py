import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll
import time
from util import epics_util as util
from tests.Tester import Tester

class M40_Tester(Tester):

    def __init__(self, path, test_name):
        
        self.path = path + str(test_name)
        Tester.__init__(self, self.path)
        self.data1 = []
        self.data2 = []
        self.stop = 1001
        self.status = PV('status')
        if test_name == 'epics':
            self.connected = True
        else:
            self.connected = util.check_device('A1', self.proc) and self.status.get() in range(0,4)
    
    def io(self):  
        if not self.connected:
            print "Device not connected"
            return False

        d_o = []
        a_o = []
        d_i = []
        a_i = []
        d_outs = {1:PV('digitalOut1'), 2:PV('digitalOut2'), 3:PV('digitalOut3'), 4:PV('digitalOut4'),
            5:PV('digitalOut5'), 6:PV('digitalOut6'), 7:PV('digitalOut7'), 8:PV('digitalOut8')}
        d_ins = {1:PV('digitalIn1'), 2:PV('digitalIn2'), 3:PV('digitalIn3'), 4:PV('digitalIn4'),
            5:PV('digitalIn5'), 6:PV('digitalIn6'), 7:PV('digitalIn7'), 8:PV('digitalIn8')}
        a_outs = {1:PV('analogOut1'), 2:PV('analogOut2'), 3:PV('analogOut3'), 4:PV('analogOut4'),
            5:PV('analogOut5'), 6:PV('analogOut6'), 7:PV('analogOut7'), 8:PV('analogOut8')}
        a_ins = {1:PV('analogIn1'), 2:PV('analogIn2'), 3:PV('analogIn3'), 4:PV('analogIn4'),
            5:PV('analogIn5'), 6:PV('analogIn6'), 7:PV('analogIn7'), 8:PV('analogIn8'),}
        poll(evt=1.e-5, iot=0.01)

        for i in range(0,8):
            d_o.append(util.put_check(d_outs[i+1], 1))
            a_o.append(util.put_check(a_outs[i+1], i))
            d_i.append(util.pv_check(d_ins[i+1], 1))
            a_i.append(a_ins[i+1].get() != None)
            

        return [x for sublist in [d_i, a_i, d_o, a_o] for x in sublist]


    def stopcount(self):
        if not self.connected:
            print "Device not connected"
            return False
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
        poll(evt=1.e-5, iot=0.01)
        analog1.wait_for_connection()
        analog2.wait_for_connection()
        init.wait_for_connection()
        stop_count.wait_for_connection()

        analog1.add_callback(getData1)

        if util.put_check(stop_count, stop):
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
        if util.put_check(stop_count, -1):
            init.put(1)
            t0 = time.time()
            while time.time() -t0 < 30:           
                poll(evt=1.e-5, iot=0.01)
        else:
            print "Stopcount not set 2nd time"
            return False

        unbuffered_run = len(data2)

        return buffered_run, unbuffered_run