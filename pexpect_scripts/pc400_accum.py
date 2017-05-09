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
		caput('initiate', 1)
		time.sleep(5)

		caput('initiate', 0)

		

	run(0)
	non_accum = data[-1] - data[-6]
	run(1)
	accum = data[-1] - data[-6]

	caput('accum_mode', 0)
	return non_accum, accum, data[0]


	
	



