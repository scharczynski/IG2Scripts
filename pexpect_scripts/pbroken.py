import subprocess
import re
import epics



def prepare(proc):


    proc.expect('\[EXCEPTION] Error parsing XML file')
    found = proc.after

    #for line in output.splitlines():
    #    if "EXCEPTION" in line:
    #        try:
    #            found = re.search('\[EXCEPTION[^:]*', line).group(0)
    #        except AttributeError:
    #            found = "no"
    return found

def test(proc):
    message = prepare(proc)
    return message
