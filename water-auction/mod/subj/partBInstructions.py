from willow.willow import *
import mod.utilities

def start(subj_id, me):
  let("")
  mod.utilities.updateStage(subj_id, "Part B instructions")

  # Show the instructions page and wait for input
  add(open("pages/subject/partb_instructions.html"))
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  mod.utilities.setPosition(subj_id, "waitingPartB")
