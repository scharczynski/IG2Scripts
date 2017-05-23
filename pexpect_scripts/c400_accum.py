from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time

def test(proc):

	data = []

	connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

	count = PV('in_counts_3')

	caput('low_limit_3', 0.0)
	caput('trig_buffer', 1000)
	caput('analog_out_period', 10e-5)
	

	def getCount(pvname, value, **kw):
		data.append(value)

	count.add_callback(getCount)


	
	time.sleep(1)

	
	def run(mode):
		
		caput('accum_mode', mode)
		time.sleep(1)

		t0 = time.time()
		while caget('accum_mode') != mode or caget('low_limit_3') != 0.0:
			if time.time() - t0 > 20:
				print "accum mode or low limit not being set"
				break

		caput('initiate', 1)
		time.sleep(5)
		caput('initiate', 0)

	

	run(0)
	if len(data) > 10:
		non_accum = data[-1] - data[-6]
	else:
		return "didnt get data"
	run(1)
	if len(data) > 10:
		accum = data[-1] - data[-6]
	else:
		return "didnt get data "

	#teardown
	while caget('accum_mode') != 0:
		caput('accum_mode', 0)
	return non_accum, accum, data[0]


	
	



