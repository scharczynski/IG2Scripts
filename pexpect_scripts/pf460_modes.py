from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time
from util import epics_util as util

def test(proc):

    data = []
    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

    util.put_check('acquisition_mode', 1)
    util.put_check('buffered_acquisition', 0)
    #util.put_check('stopcount', 1000)

    current1 = PV('current_in_1')

	def getCount(pvname, value, **kw):
		data.append(value)

	current1.add_callback(getCount)

	util.put_check('initiate', 1)
	
    

	t0 = time.time()
	while time.time() - t0 < 30 and len(data) < 3000:
		pass
	
	caput('initiate', 0)

	time.sleep(0.5)


	return len(data), caget('stopped_state'), caget('running_state')
	



    





