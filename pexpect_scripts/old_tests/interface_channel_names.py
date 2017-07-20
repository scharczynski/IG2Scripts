import time
from epics import caput, caget, PV
import pexpect

def test(proc): 

    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

    test1 = PV('name1')
    test2 = PV('name2')
    test3 = PV('name3')

    return [test1.pvname==test1.value, test2.pvname==test2.value, test3.pvname==test3.value]


