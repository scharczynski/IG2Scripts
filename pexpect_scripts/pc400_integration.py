from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time

def test(proc):

	data = []
	connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

	count = PV('in_counts_3')

	caput('trig_mode', 1)
	caput('low_limit_3', 0.0)
	caput('low_limit_4', 0.0)
	caput('trig_buffer', 1000)
	caput('analog_out_period', 10e-5)


	def getCount(pvname, value, **kw):
		data.append(value)


	count.add_callback(getCount)

	caput('initiate', 1)
	time.sleep(2)

	fast = count.value

	caput('analog_out_period', 10e-3)
	caput('initiate', 1)
	time.sleep(5)

	slow = count.value
	
	return slow/(fast + 0.01*fast), slow/(fast - 0.01*fast)