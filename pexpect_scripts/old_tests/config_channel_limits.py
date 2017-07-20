from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time

def test(proc):
	proc.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=3)

	data1 = []
	data2 = []
	data3 = []

	test1 = PV('test1')
	test2 = PV('test2')
	test3 = PV('test3')

	test1.put('-1')
	time.sleep(0.1)
	data1.append(proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

	test1.put('6')
	time.sleep(0.1)
	data1.append(proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

	test1.put('5')
	time.sleep(0.1)
	data1.append(proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

	test2.put('-11')
	time.sleep(0.1)
	data2.append(proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

	test2.put('-1')
	time.sleep(0.1)
	data2.append(proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

	test2.put('-3')
	time.sleep(0.1)
	data2.append(proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

	test3.put('10')
	time.sleep(0.1)
	data3.append(proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

	test3.put('-10')
	time.sleep(0.1)
	data3.append(proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=1))

	test3.put('0')
	time.sleep(0.1)
	data3.append(proc.expect(['Limit violation', pexpect.TIMEOUT, pexpect.EOF], timeout=5))


	return [x+y+z for x,y,z in zip(data1, data2, data3)]