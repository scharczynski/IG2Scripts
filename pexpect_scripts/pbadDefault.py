import re
from epics import caget, caput, PV, ca, get_pv, pv
import os
import datetime
import pexpect

def test(proc):

    proc.expect('\[EXCEPTION[^:]*string')
    error = proc.after
    return error
