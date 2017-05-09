from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time

def test(proc):

	data = []

	connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

	count = PV('in_counts_3')

	caput('trig_mode', 1)
	caput('low_limit_3', 0.0)
	caput('trig_buffer', 0)
	caput('analog_out_period', 10e-5)

	def getCount(pvname, value, **kw):
		data.append(value)

	count.add_callback(getCount)

	caput('initiate', 1)
	time.sleep(1)

	t0 = time.time()
	while time.time() - t0 < 30 and len(data) < 3000:
		pass
	
	caput('initiate', 0)

	time.sleep(0.5)

	return len(data), caget('stopped_state'), caget('running_state')
	





