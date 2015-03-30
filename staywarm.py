import requests
import json
import time
import os
import sys
from threading import Thread

# update these for your environment
apiurl = "http://octoprint:5000/api"
apikey = "EA1354A4D39E475D86A62E07C00A146E"
pidfile = "/tmp/staywarm.pid"
max_on_time = "60" # minutes

# thread
def run():
    on_time = 0
    while on_time < max_on_time:
	# get temps
	uri = apiurl + "/printer"
	headers = { 'Content-type': 'application/json', 'X-Api-Key': apikey }
	r = requests.get(uri, headers=headers)
	
	if r.status_code >= 400:
	  print "Error: couldn't get temperature from API"
	  return

	j = r.json()

	# set target temp if there is one
	if j['temperature']['temps']['bed']['target'] is not None:
	  uri = apiurl + "/printer/bed"
	  body = { 'command': 'target', 'target': j['temperature']['temps']['bed']['target'] }
	  r = requests.post(uri, headers=headers, data=json.dumps(body))

	if j['temperature']['temps']['tool0']['target'] is not None:
	  uri = apiurl + "/printer/tool"
	  body = { 'command': 'target', 'targets': { 'tool0': j['temperature']['temps']['tool0']['target'] } }
	  r = requests.post(uri, headers=headers, data=json.dumps(body))
	
	time.sleep(60)
        on_time += 1
    print "Maximum specified heater timeout has been reached, exiting." 

def check_pid(pid):        
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError):
        return False
    else:
        return True

if __name__ == "__main__":
# check if we are already running, stop running process and spawn a new one unless we are turning off
 if os.path.isfile(pidfile):
  p = open(pidfile, "r")
  oldpid = p.readline()
  if check_pid(oldpid):
    print "found staywarm pid %s, killing it" % oldpid
    os.kill(int(oldpid), 9)
  os.unlink(pidfile) 
 
 if len(sys.argv) > 1 and sys.argv[1] == "off": 
   sys.exit()

# fork into the background and keep setting the temp every 30 seconds (turn on)
 pid = os.fork()
 if(pid == 0):
  os.chdir("/")
  os.setsid()
  os.umask(0)
  pid2 = os.fork()
  if(pid2 == 0):
    t = Thread(target=run, args=())
    t.start()
    mypid = os.getpid()
    print "Forked to child pid %d" % mypid
    f = file(pidfile, "w")
    f.write("%d" % mypid)
    f.close()
    sys.exit()
  else:
    sys.exit()
 else:
  sys.exit()
