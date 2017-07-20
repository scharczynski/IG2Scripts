from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time

def test(proc):

    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)
    
    return caget('firmware_version'), caget('fpga_version'), caget('serial_number'), caget('software_rev'), caget('secondary_fpga_version'), caget('rpt_revision'), caget('hardware_revision')