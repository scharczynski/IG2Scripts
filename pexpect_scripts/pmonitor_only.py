from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time


def test(proc):

	connect = proc.expect(['Announce\(\) success', pexpect.TIMEOUT, pexpect.EOF], timeout=3)

	#print proc.after


	count3 = PV('in_counts_3')
	count4 = PV('in_counts_4')

	#print count3.value,count4.value

	data3 = []
	data4 = []

	caput('trig_mode', 1)
	caput('low_limit_3', 0.0)
	caput('low_limit_4', 0.0)
	caput('trig_buffer', 1000)
	caput('analog_out_period', 10e-5)

	t0 = time.time()
	while caget('trig_buffer')!=1000 and caget('trig_mode')!=1 and time.time()-t0 < 20:
		pass


	#print caget('low_limit_3'), caget('low_limit_4'), caget('trig_buffer'), caget('analog_out_period'), caget('trig_mode')

	def getCount3(pvname, value, **kw):
		data3.append(value)

	def getCount4(pvname, value, **kw):
		data4.append(value)

	count3.add_callback(getCount3)
	count4.add_callback(getCount4)

	caput('initiate', 1)
	time.sleep(3)

	#print data4

	return len(data3), len(data4)