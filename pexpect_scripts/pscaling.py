from epics import caget, caput, PV, ca, get_pv, pv
import pexpect
import time
import math

def test(proc):

	proc.expect(['Announce\(\) success', pexpect.TIMEOUT, pexpect.EOF], timeout=3)

	normal = PV('cleanIn1')
	linear = PV('linearIn1')
	log = PV('logIn1')
	both_scaled = PV('bothScaled')

	caput('initiate', 1)

	time.sleep(2)

	base = normal.get()
	lin = linear.get()
	logged = log.get()
	both = both_scaled.get()

	print base, lin, logged, both

	print base, ((lin-1000)/200), logged ** 10, ((both ** 10) - 1000)/200

	print base, base*200 + 1000, math.log(base,10), math.log((base*200+1000), 10)

