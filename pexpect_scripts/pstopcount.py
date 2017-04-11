import epics
import signal
import time
from epics import caput, caget, PV, ca, pv, camonitor, camonitor_clear
import pexpect



def test(proc):
	while caget('status') != 0:
		time.sleep(0.1)
		print "device not ready"
	#proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=3)
	stop = 100
	data1 = []
	data2 = []
	
	caput('outStopCount', 100)
	time.sleep(1)
	#caput('outStopCount', 100)
	testtime = time.time()
	caget('analogIn1')
	caget('analogIn2')
	while caget('outStopCount') != 100 and time.time() - testtime < 40:
		print "waiting" + str(caget('outStopCount'))
		caput('outStopCount', 100)
		#caput('outStopCount', 100)
		

	print (time.time() - testtime)

	def getData(pvname, value, **kw):
		if '1' in pvname and value != 0:
			data1.append(value)
		if '2' in pvname and value != 0:
			data2.append(value)


	def looper():
		t0 = time.time()
		while time.time() -t0 < 10	:
			epics.poll(evt=1.e-5, iot=0.01)

	#def event_append():
	#	print 'in loop2'
	#	t0 = time.time()
	#	while time.time() -t0 < 10:
	#		new = caget('analogIn1')

	#		if new != data1[-1]:
	#			getData('analogIn1', caget('analogIn1'))
			

	analog1 = PV('analogIn1')
	init = PV('initiate')
	#stopcount = PV('outStopCount')
	analog2 = PV('analogIn2')

	analog1.wait_for_connection()
	analog2.wait_for_connection()
	init.wait_for_connection()
	#stopcount.wait_for_connection()

	analog1.add_callback(getData)
	analog2.add_callback(getData)
	#init.add_callback(looper)



	#stopcount.put(stop, wait=True)
	
	#time.sleep(2)
	print caget('outStopCount')
	#print stopcount.value

	init.put(1, use_complete=True)

	

	#print data1	
	print caget('outStopCount')
	looper()	
	return (len(data1), len(data2))
#print test("hi")