from willow.willow import *

def start(me):

  # Put inital dictionaries on to the stack
  put({"tag": "numStarted", "num": 0, "clients": []})
  put({"tag": "numFinished", "num": 0, "clients": []})

  # Open up the display and then wait until the proctor wants to finish the 
  # experiment
  add(open("pages/monitor/monitor.html"))
  take({"tag": "click", "id": "finish", "client": me})

  # Check out the choice and then depending on the number (btwn 1 and 6) decide 
  # on how to handle client data and gather all data from clients that they have posted in
  choice = peek("#resultInput")
  clientsFinished = take({"tag": "numFinished"})
  clientData = []
  for client in clientsFinished["clients"]:
    clientData.append(take({"client": client, "tag": "clientData"}))

  #let(clientData, "#data")
  put({"finish": "true", "client": me, "choice": choice})


