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


	return (check(lin, base*2 + 10, 0.01) and check(logged, 10**base, 0.01) and check(both, 10 ** (base*2 +10), 0.01))





def check(value1, value2, tolerance):
	mod_plus = value1 + value1*tolerance
	mod_minus = value1 - value1*tolerance

	return (mod_plus >= value2 or mod_minus <= value2)