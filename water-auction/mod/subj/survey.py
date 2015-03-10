from willow.willow import *
import mod.utilities

def start(subj_id, me):
  mod.utilities.updateStage(subj_id, "Final Survey")
  let("")
  add(open("pages/subject/survey.html"))
  take({"client": me, "id": "continue", "tag": "click"})
  let("")
  mod.utilities.setPosition(subj_id, "last page")
  mod.utilities.updateStage(subj_id, "END")
  add(open("pages/subject/final.html"))
