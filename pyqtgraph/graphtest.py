"""
Display a plot and an image with minimal setup.

pg.plot() and pg.image() are indended to be used from an interactive prompt
to allow easy data inspection (but note that PySide unfortunately does not
call the Qt event loop while the interactive prompt is running, in this case
it is necessary to call QApplication.exec_() to make the windows appear).
"""


import re
from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import os
import datetime
import pexpect
import numpy as np
import pyqtgraph as pg
import time




#print caget('digitalIn1')
#print caget('digitalIn2')
#print caget('digitalIn3')
#print caget('digitalIn4')
#print caget('analogIn1')
#print caget('analogIn2')

#caput('digitalOut1', 1)
#caput('digitalOut2', 1)
#caput('digitalOut3', 1)
#caput('digitalOut4', 1)
#print caget('digitalOut1')
#print caget('digitalOut2')
#print caget('digitalOut3')
#print caget('digitalOut4')

#caput('analogOut1', 5)
#caput('analogOut2', 9)
#print caget('analogOut1')
#print caget('analogOut2')
#return 45

y1 = []
y2 = []
len1 = 0
len2 = 0

def getData(pvname, value, **kw):
    if '1' in pvname:
        y1.append(value)
        #print "value change"
    if '2' in pvname:
        y2.append(value)


camonitor('analogIn1', callback=getData)
camonitor('analogIn2', callback=getData)





app = pg.QtGui.QApplication([])
win = pg.GraphicsWindow(title="analog1In")
win2 = pg.GraphicsWindow(title="analog2In")
pg.setConfigOptions(antialias=True)

#p = pg.plot()
#p2 = pg.plot()
#curve = p.plot()
#curve2 = p2.plot()

p1 = win.addPlot()
p2 = win2.addPlot()

curve1 = p1.plot()
curve2 = p2.plot()

data = [0,0]

#data2 = [0]

#win = pg.GraphicsWindow(title="Basic plotting examples")
#win.resize(1000,600)
#win.setWindowTitle('pyqtgraph example: Plotting')
#pg.setConfigOptions(antialias=True)

#p1 = win.addPlot(title="analogin1")
#p2 = win.addPlot(title="analogin2")
#curve = p1.plot(pen='r')
#curve2 = p2.plot(pen='r')
curve1.setPos(0, 0)
n = 10
number = 0
x1 = 0
x2 = 200
len1 = 0
len2 = 0
def updater():
    global number, curve1, curve2, y1, y2, x1, x2, len1, len2
    #value = caget('analogIn1')
    #value2 = caget('analogIn2')

    #y1.append(caget('analogIn1'))
    #y2.append(caget('analogIn2'))
    #print "len1 is " + str(len1)
    #print "length is " + str(len(y1))
    #data2.append(value2)
    #y1[:-1] = y1[1:]
    #y2[:-1] = y2[1:]
    #narr = np.roll(narr, 1)
    #data2.append(caget('analogIn2'))
    if len1 < len(y1):
        curve1.setData(np.array(y1)) #xdata is not necessary
        len1 += 1
    if len2 < len(y2):
        curve2.setData(np.array(y2))
        len2 += 1
    #curve2.setData(np.asarray(data2))
    #curve2.setPos(len(y2), 0)
    #curve1.setPos(len(y1), 0)

    p1.setXRange(len(y1)-200, len(y1))
    p2.setXRange(len(y2)-200, len(y2))
    #print timer
    number += 1
    app.processEvents()

timer = pg.QtCore.QTimer()
timer.timeout.connect(updater)
timer.start(0)


#print data

#print data
#data = np.random.normal(size=1000)
#pg.plot(np.asarray(data), title="Simplest possible plotting example")



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
