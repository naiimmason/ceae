from willow.willow import *
import mod.utilities

def start(subj_id, me):
  let("")
  # Open waiting landing page and wait for advance packet before moving on and
  # updating the numbers
  mod.utilities.updateStage(subj_id, "Waiting for practice")
  add(open("pages/subject/landing.html"))
  advance = take({"advance": True, "stage": "waitingPractice1"})
  put(advance)
  mod.utilities.setPosition(subj_id, "practiceInput1")
