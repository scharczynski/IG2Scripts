import math
import epics
import pexpect
import numpy as np
import matplotlib.pyplot as plt
import time


proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/m10_signal.xml")
time.sleep(2)
connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'Announce\(\) success'], timeout=5)

out1 = epics.PV('analogOut1')
t = 0  
omega = 2*np.pi*(1)
data = []
times = np.arange(0, 600, 0.01)
wave = np.sin(np.arange(0, omega*0.01*60000, omega*0.01))
model = []



for x in wave:
    t0 = time.time()
    #t = time.time()
    #print t-t0
    #value = (np.sin(omega*t))
    value = x
    out1.put(value)
    #times.append(t)
    #model.append(value)
    #t += 0.001
    data.append(out1.get())
    #print data
    if time.time()-t0 < 0.01:        
        time.sleep(-time.time()+t0+0.01)
    else:
        print "loop too long"

print len(data)
print len(times)
print time.time()-t0
plt.plot(times, data)
plt.show()


#print times
# Fs = 8000
# f = 5
# sample = 8000
# x = np.arange(sample)
# y = np.sin(2 * np.pi * f )
# plt.plot(x, y)
# plt.xlabel('voltage(V)')
# plt.ylabel('sample(n)')
# plt.show()