import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll
import time
from util import epics_util as util
from tests.Tester import Tester

class M10_Tester(Tester):
    
    def __init__(self, path, test_name):
        #self.proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/"+name+".xml")
        Tester.__init__(self, path)
        self.path += str(test_name) + ".xml"
        self.proc = pexpect.spawn(self.path)
        self.data1 = []
        self.data2 = []
        self.stop = 1001
        # self.on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=CCL"')
        # self.on2 = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?2=CCL"')


    def io(self):
        # on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=CCL"')
        # on2 = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?2=CCL"')
        #self.proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/m10_io.xml")
        self.proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=3)

        d_i = []
        a_i = []
        d_o = []
        a_o = []

        caput('initiate', 1)
        
        for i in range(0,4):
            d_o.append(util.put_check('digitalOut' + str(i+1), 1))
            d_i.append(util.pv_check('digitalIn'+ str(i+1), 1))
            

        for i in range(0,2):
            a_o.append(util.put_check('analogOut' + str(i+1), i))
            a_i.append(caget('analogIn'+ str(i+1)) != None)


        return [x for sublist in [d_i, a_i, d_o, a_o] for x in sublist]

    # def getData1(pvname, value, **kw):
    #     if value != 0:
    #         self.data1.append(value)

    # def getData2(pvname, value, **kw):
    #     if value != 0:
    #         self.data2.append(value)
    

    def stopcount(self):
        #self.proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/m10_stopcount.xml")
        self.proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=10)
        

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

        analog1.wait_for_connection()
        analog2.wait_for_connection()
        init.wait_for_connection()
        stop_count.wait_for_connection()

        analog1.add_callback(getData1)
        

        

        
        if util.put_check('outStopCount', self.stop):
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
        if util.put_check('outStopCount', -1):
            init.put(1)
            t0 = time.time()
            while time.time() -t0 < 30:           
                poll(evt=1.e-5, iot=0.01)
        else:
            print "Stopcount not set 2nd time"
            return False

        unbuffered_run = len(self.data2)

        return buffered_run, unbuffered_run


