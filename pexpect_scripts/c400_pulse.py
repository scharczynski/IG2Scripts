from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time
from util import epics_util as util

def test(proc):

	data = []
	connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

	time.sleep(1)

	print util.put_check('pulse_period', 10000)
	put = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)
	print proc.before
	util.put_check('pulse_width', 100)
	util.put_check('digital_out_pulse_enable_1', 1)
	util.put_check('digital_out_pulse_enable_2', 1)
	util.put_check('digital_out_pulse_enable_3', 1)
	util.put_check('digital_out_pulse_enable_4', 1)

	print caget('pulse_period')
	print caget('pulse_width')
	print caget('digital_out_pulse_enable_1')
	print caget('digital_out_pulse_enable_2')
	print caget('digital_out_pulse_enable_3')
	print caget('digital_out_pulse_enable_4')

	period = caget('pulse_period')
	width = caget('pulse_width')
	p1 = caget('digital_out_pulse_enable_1')
	p2 = caget('digital_out_pulse_enable_2')
	p3 = caget('digital_out_pulse_enable_3')
	p4 = caget('digital_out_pulse_enable_4')

	#teardown
	util.put_check('digital_out_pulse_enable_1', 0)
	util.put_check('digital_out_pulse_enable_2', 0)	
	util.put_check('digital_out_pulse_enable_3', 0)
	util.put_check('digital_out_pulse_enable_4', 0)
	util.put_check('pulse_period', 100)
	util.put_check('pulse_width', 1)

	return [period, width, p1, p2, p3, p4]


