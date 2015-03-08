from willow.willow import *
import mod.utilities

def start(subj_id, me):
  let("")
  # Update the stage and add the view
  mod.utilities.updateStage(subj_id, "Waiting for Part C")
  add(open("pages/subject/btwnparts.html"))

  # Put current data on stack for analysis before moving on
  clientData1 = { "user": subj_id, "client": me, "tag": "clientData1", 
    "results": mod.utilities.grabInfo(subj_id)["results"] }
  put(clientData1)

  # Wait for the advance token and update position
  advance = take({"advance": True, "stage": "waitingPartC"})
  put(advance)
  mod.utilities.setPosition(subj_id, "partCWater1")
