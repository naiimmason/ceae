from willow.willow import *
import mod.utilities

def start(subj_id, me):
  let("")
  mod.utilities.updateStage(subj_id, "Part C instructions")

  # Show the instructions page and wait for input
  add(open("pages/subject/partc_instructions.html"))

  communication = take({"tag": "communication"})
  put(communication)
  if communication["communication"]:
    add("You will be given 5 minutes time for communication within your group before each task. The experimenter will announce the beginning and end of the 5 minutes communication time. Once the 5 minutes are over, no further communication is permitted.","#comm")
    
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  mod.utilities.setPosition(subj_id, "waitingPartC")
