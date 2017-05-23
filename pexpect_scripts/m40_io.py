import re
from epics import caget, caput, PV, ca, get_pv, pv
import os
import datetime
import pexpect
import time
from util import epics_util as util

def test(proc):
    proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=3)

    d_o = []
    a_o = []
    d_i = []
    a_i = []

    for i in range(0,8):
        d_o.append(util.put_check('digitalOut' + str(i+1), 1))
        a_o.append(util.put_check('analogOut' + str(i+1), i))
        d_i.append(util.pv_check('digitalIn'+ str(i+1), 1))
        a_i.append(util.pv_check('analogIn'+ str(i+1), 0.0))
        

    return [x for sublist in [d_i, a_i, d_o, a_o] for x in sublist]
