from willow.willow import *
import mod.utilities

def input1(subj_id, me):
  mod.utilities.setPosition(subj_id, "waitingPracticeResults1")
  return "hello"

def waitingResults1(subj_id, me):
  mod.utilities.setPosition(subj_id, "practiceResults1")
  return "hello"

def results1(subj_id, me):
  mod.utilities.setPosition(subj_id, "waitingPractice2")
  return "hello"

def waitingPractice2(subj_id, me):
  mod.utilities.setPosition(subj_id, "practiceInput2")
  return "hello"

def input2(subj_id, me):
  mod.utilities.setPosition(subj_id, "waitingPracticeResults2")
  return "hello"

def waitingResults2(subj_id, me):
  mod.utilities.setPosition(subj_id, "practiceResults2")
  return "hello"

def results2(subj_id, me):
  mod.utilities.setPosition(subj_id, "partBInstructions")
  return "hello"

