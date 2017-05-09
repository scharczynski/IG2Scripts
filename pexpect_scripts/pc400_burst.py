from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time

def test(proc):

	proc.expect(['Announce\(\) success', pexpect.TIMEOUT, pexpect.EOF], timeout=3)

	data = []

	count = PV('in_counts_3')

	caput('low_limit_3', 0.0)
	caput('analog_out_period', 10e-4)
	caput('trig_burst', 1000)
	caput('trig_buffer', 0)

	def getCount(pvname, value, **kw):
		data.append(value)

	count.add_callback(getCount)

	caput('initiate', 1)
	while caget('paused_state') != 1:
		
		pass
	print len(data)		


	print caget('running_state'), caget('paused_state'), caget('stopped_state')
	#print data
