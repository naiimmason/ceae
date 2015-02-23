from willow.willow import *

def start(me):
  put({"tag": "numStarted", "num": 0})
  put({"tag": "numFinished", "num": 0})
  add(open("pages/monitor/monitor.html"))
  take({"tag": "click", "id": "finish", "client": me})
  put({"finish": "true", "client": me})


