import epics
import signal
import time
from epics import caput, caget, PV, ca, pv, camonitor, camonitor_clear
import pexpect



def test(proc):


	ccl1 = pexpect.spawn('curl "http://admin:1234@192.168.100.36/outlet?1=CCL"')
	time.sleep(2)
	proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=30)
	#print proc.after
	#time.sleep(10)
	
	while caget('status') != 0:
		time.sleep(0.1)
		#print "device not ready"
	
	stop = 1000
	data1 = []
	data2 = []
	
	def getData(pvname, value, **kw):
		if '1' in pvname and value != 0:
			data1.append(value)
		if '2' in pvname and value != 0:
			data2.append(value)

	def getData1(pvname, value, **kw):
		if value != 0:
			data1.append(value)

	def getData2(pvname, value, **kw):
		if value != 0:
			data2.append(value)


	def looper():
		t0 = time.time()
		while time.time() -t0 < 20:
			epics.poll(evt=1.e-5, iot=0.01)



	analog1 = PV('analogIn1')
	stop_count = PV('outStopCount')
	init = PV('initiate')
	analog2 = PV('analogIn2')

	analog1.wait_for_connection()
	analog2.wait_for_connection()
	init.wait_for_connection()
	stop_count.wait_for_connection()

	analog1.add_callback(getData1)
	analog2.add_callback(getData2)

	def onPutComplete(pvname=None, **kws):
		return True
    	#print 'Put done for %s' % pvname

	#def checkStop():
	#	testtime = time.time()
	#	while time.time() - testtime < 50:
	#		if caget('outStopCount') == stop:
	#			epics.poll(evt=1.e-5, iot=0.01)
	#			return True
	#		else:
	#			caput('outStopCount', stop)
	#	return False
	t0 = time.time()
	while time.time() -t0 < 50:
		
		if stop_count.put(stop, callback=onPutComplete):
			epics.poll(evt=1.e-5, iot=0.01)
		else:
			pass
			#print "waiting for count to set"
	
	#while caget('outStopCount') != stop and time.time() - testtime < 40:
		#print "waiting" + str(caget('outStopCount'))
		#print (time.time() - testtime)
	#	caput('outStopCount', stop)
		#caput('outStopCount', 100)
		

	#init.add_callback(looper)
	#print (time.time() - testtime)

	#looper()

	

	#def event_append():
	#	print 'in loop2'
	#	t0 = time.time()
	#	while time.time() -t0 < 10:
	#		new = caget('analogIn1')

	#		if new != data1[-1]:
	#			getData('analogIn1', caget('analogIn1'))
			

	



	#stopcount.put(stop, wait=True)
	
	#time.sleep(2)
	#print caget('outStopCount')
	#print stopcount.value

	#init.put(1, use_complete=True)

	

	
	
	#print data1

	#print caget('outStopCount')
	return (len(data1), len(data2))
#print test("hi")