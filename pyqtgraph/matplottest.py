import numpy as np
import matplotlib.pyplot as plt
from epics import caget, caput, PV, ca, get_pv, pv



plt.axis([0,400,0.001, 0.002])
plt.ion()


for i in range(400):
    y = caget('analogIn1')
    plt.scatter(i, y)
    plt.pause(0.05)

while True:
    plt.pause(0.05)
