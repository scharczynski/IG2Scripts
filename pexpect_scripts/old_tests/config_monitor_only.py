from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time
from util import epics_util as util


def test(proc):

	#cycle = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?3=CCL"')

	connect = proc.expect(['Announce\(\) success', pexpect.TIMEOUT, pexpect.EOF], timeout=4)

	#print proc.after


	count3 = PV('in_counts_3')
	count4 = PV('in_counts_4')

	#print count3.value,count4.value

	data3 = []
	data4 = []

	util.put_check('trig_mode', 1)
	util.put_check('low_limit_3', 0.0)
	util.put_check('low_limit_4', 0.0)
	util.put_check('trig_buffer', 1000)
	util.put_fuzzy('analog_out_period', 10e-5, 0.01)


	#print caget('low_limit_3'), caget('low_limit_4'), caget('trig_buffer'), caget('analog_out_period'), caget('trig_mode')

	def getCount3(pvname, value, **kw):
		data3.append(value)

	def getCount4(pvname, value, **kw):
		data4.append(value)

	count3.add_callback(getCount3)
	count4.add_callback(getCount4)

	util.put_check('initiate', 1)
	time.sleep(3)

	#print data4

	return len(data3), len(data4)