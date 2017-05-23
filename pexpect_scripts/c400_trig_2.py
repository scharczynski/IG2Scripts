from epics import caget, caput, PV, ca, get_pv, pv, camonitor
import pexpect
import time
from util import epics_util as util


def test(proc):

    data = []
    connect = proc.expect([pexpect.TIMEOUT, pexpect.EOF,
                           'Announce\(\) success'], timeout=5)
    # caput('trig_mode', 1)
    #print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')

    util.put_check('trig_source_start', 0)
    util.put_check('trig_source_pause', 0)
    util.put_check('trig_source_stop', 0)
    util.put_check('trig_mode', 0)

    #print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')

    for i in range(0, 4):
        puti = util.put_check('trig_source_start', i)

        for j in range(0, 4):
            bad = 0
            putj = util.put_check('trig_source_pause', j)

            for k in range(0, 4):
                if j == k and k != 0:
                    caput('trig_source_stop', k)
                    bad = proc.expect(
                        [pexpect.TIMEOUT, "Error setting C400 configuration"], timeout=5)
                   
                    if bad == 1:
                        putk = True
                    else:
                        putk = False
                else:
                    putk = util.put_check('trig_source_stop', k)
                
                if puti and putk and putj:
                    data.append(True)
                else:
                    data.append(False)

                #print (i, j, k)
                #print caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')
                #print puti, putj, putk
            util.put_check('trig_source_stop', 0)
                # if not(util.put_check('trig_source_stop', k)):  #
                # time.sleep(0.1)

                #     else:
                #         #print str(k) + ":kFasle"
                #         #print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')
                #         data.append(False)
                # else:
                #     data.append(True)

                # if not(util.put_check('trig_source_start', i)):
                #     #print str(k) + ":iFasle"
                #     #print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')
                #     data.append(False)
                # else:
                #     data.append(True)

                # if not(util.put_check('trig_source_pause', j)):
                #     #print str(k) + ":jFasle"
                #     #print caget('trig_mode'), caget('trig_source_start'), caget('trig_source_pause'), caget('trig_source_stop')
                #     data.append(False)
                # else:
                #     data.append(True)
                # data.append((caget('trig_source_start'), caget(
                #     'trig_source_pause'), caget('trig_source_stop')))

        #     util.put_check('trig_source_stop', 0)
        # util.put_check('trig_source_pause', 0)

    for i in range(0, 7):
        #print i
        util.put_check('trig_mode', i)
        time.sleep(1)
        if caget('trig_mode') != i:
            data.append(True)

    #print data

    # teardown

    util.put_check('trig_mode', 1)
    util.put_check('trig_burst', 0)

    if all(x == True for x in data):
        return True
    else:
        #print data
        return False
