from willow.willow import *
import mod.utilities

def start(subj_id):
  let("")
  # Update the stage and add the view
  mod.utilities.updateStage(subj_id, "Waiting for Part B")
  add(open("pages/subject/waitingPartB.html"))

  # Wait for the advance token and update position
  advance = take({"advance": True, "stage": "waitingPartB"})
  put(advance)
  mod.utilities.setPosition(subj_id, "partBWater1")
