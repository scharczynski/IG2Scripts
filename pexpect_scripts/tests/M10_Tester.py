import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll
import time
from util import epics_util as util
from tests.Tester import Tester

class M10_Tester(Tester):
    
    def __init__(self, path, test_name):
        #self.proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/"+name+".xml")
        if test_name == 'epics':
            self.path = path
        else:
            self.path = path + str(test_name)
        print self.path
        Tester.__init__(self, self.path)
        self.data1 = []
        self.data2 = []
        self.stop = 1001
        self.status = PV('status')
        if test_name == 'epics':
            self.connected = True
        else:
            self.connected = util.check_device('A1', self.proc) and self.status.get() in range(0,4)

        # self.on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=CCL"')
        # self.on2 = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?2=CCL"')





    def io(self):
        # on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=CCL"')
        # on2 = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?2=CCL"')
        #self.proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/m10_io.xml")

        if not self.connected:
            print "Device not connected"
            return False
        init = PV('initiate')
        d_outs = {1:PV('digitalOut1'), 2:PV('digitalOut2'), 3:PV('digitalOut3'), 4:PV('digitalOut4')}
        d_ins = {1:PV('digitalIn1'), 2:PV('digitalIn2'), 3:PV('digitalIn3'), 4:PV('digitalIn4')}
        a_ins = {1:PV('analogIn1'), 2:PV('analogIn2'), 3:PV('analogIn3'), 4:PV('analogIn4')}
        a_outs = {1:PV('analogOut1'), 2:PV('analogOut2'), 3:PV('analogOut3'), 4:PV('analogOut4')}
        # dout1, dout2, dout3, dout4 = PV('digitalOut1'), PV('digitalOut2'), PV('digitalOut3'),  PV('digitalOut4')
        # din1, din2, din3, din4 = PV('digitalIn1'), PV('digitalIn2'), PV('digitalIn3'), PV('digitalIn4')
        # aout1, aout2, aout3, aout4 = PV('analogOut1'), PV('analogOut2'), PV('analogOut3'), PV('analogOut4')
        # ain1, ain2, ain3, ain4 = PV('analogIn1'), PV('analogIn2'), PV('analogIn3'), PV('analogIn4')
        poll(evt=1.e-5, iot=0.01)
        d_i = []
        a_i = []
        d_o = []
        a_o = []

        init.put(1)
        poll(evt=1.e-5, iot=0.01)
        for i in range(0,4):
            d_o.append(util.put_check(d_outs[i+1], 1))
            d_i.append(util.pv_check(d_ins[i+1], 1))
            

        for i in range(0,2):
            a_o.append(util.put_check(a_outs[i+1], i))
            a_i.append(a_ins[i+1].get() != None)

        print d_o
        return [x for sublist in [d_i, a_i, d_o, a_o] for x in sublist]

    # def getData1(pvname, value, **kw):
    #     if value != 0:
    #         self.data1.append(value)

    # def getData2(pvname, value, **kw):
    #     if value != 0:
    #         self.data2.append(value)
    

    def stopcount(self):
        #self.proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/m10_stopcount.xml")

        if not self.connected:
            print "Device not connected"
            return False

        #util.pv_check('status', 0)
        
        #self.stop = 1001


        def getData1(pvname, value, **kw):
            if value != 0:
                self.data1.append(value)

        def getData2(pvname, value, **kw):
            if value != 0:
                self.data2.append(value)

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
        

        

        
        if util.put_check(stop_count, self.stop):
            init.put(1)
            t0 = time.time()
            while time.time() -t0 < 30:           
                poll(evt=1.e-5, iot=0.01)
        else:
            print "Stopcount not set"
            return False

        buffered_run = len(self.data1)
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

        unbuffered_run = len(self.data2)
        print unbuffered_run, buffered_run
        return buffered_run, unbuffered_run


