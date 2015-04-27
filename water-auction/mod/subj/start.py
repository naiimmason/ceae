from willow.willow import *
import mod.utilities

def start(subj_id, me):
  mod.utilities.updateStage("subj_id", "Practice instructions")

  # Show first instruction page and wait for them to continue
  add(open("pages/subject/prac_instructions.html"))
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  # Update number of people who are waiting to start
  mod.utilities.increment("numStart", me)
  mod.utilities.setPosition(subj_id, "waitingPractice1")
