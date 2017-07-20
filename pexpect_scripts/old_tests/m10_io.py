from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time
from util import epics_util as util

def test(proc):
    proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=3)

    d_i = []
    a_i = []
    d_o = []
    a_o = []


    for i in range(0,4):
        d_o.append(util.put_check('digitalOut' + str(i+1), 1))
        d_i.append(util.pv_check('digitalIn'+ str(i+1), 1))
        

    for i in range(0,2):
        a_o.append(util.put_check('analogOut' + str(i+1), i))
        a_i.append(caget('analogIn'+ str(i+1)) != None)

   
    return [x for sublist in [d_i, a_i, d_o, a_o] for x in sublist]


