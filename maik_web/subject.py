from willow.willow import *
import reconnect
import random as rand

# Checks to see if an input is a valid float number inside of a certain range
def isValid(input):
  try:
    truth = float(input) >= 0.0 and float(input) <= 5000.0
    return truth
  except ValueError:
    return False

def start(me, subj_id, data_filepath1, survey_filepath1):
  let("")
  add(open("pages/subject.html"))


  pop("hidden", ".part1_questions")

  return "hello"
