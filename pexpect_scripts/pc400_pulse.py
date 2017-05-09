from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time

def test(proc):

	data = []
	connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

	print caget('pulse_period')
	print caget('pulse_width')
	print caget('digital_out_pulse_enable_1')
	print caget('digital_out_pulse_enable_2')
	print caget('digital_out_pulse_enable_3')
	print caget('digital_out_pulse_enable_4')

	caput('digital_out_pulse_enable_1', 1)
	caput('digital_out_pulse_enable_2', 1)
	caput('digital_out_pulse_enable_3', 1)
	caput('digital_out_pulse_enable_4', 1)

	time.sleep(2)


	print caget('pulse_period')
	print caget('pulse_width')
	print caget('digital_out_pulse_enable_1')
	print caget('digital_out_pulse_enable_2')
	print caget('digital_out_pulse_enable_3')
	print caget('digital_out_pulse_enable_4')