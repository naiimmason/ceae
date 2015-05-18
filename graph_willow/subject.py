from willow.willow import *
import reconnect
import random as rand

def start(me, subj_id, data_filepath1, survey_filepath1):
  let("")
  add(open("pages/subject.html"))

  if reconnect.getPosition(subj_id) == "start":
    pop("hidden", ".instructions")
  
  return "hello"
