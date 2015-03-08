from willow.willow import *
import mod.utilities

practice_items = [
  "eat a piece of candy",
  "draw a picture"
]

# Checks to see if an input is a valid float number inside of a certain range
def isValid(input):
  try:
    truth = float(input) >= 0.0 and float(input) <= 5000.0
    return truth
  except ValueError:
    return False

def input(subj_id, me, practice_id):
  let("")
  mod.utilities.updateStage(subj_id, "Practice " + str(practice_id + 1) +" input")
  add(open("pages/subject/practice_input.html"))
  let(practice_items[practice_id], "#practiceItem")

  offer = -1
  # Wait for the client to submit an offer
  offer = -1
  while offer == -1:
    take({"tag": "click", "id": "submit", "client": me})

    # Look at the offer and check if it is a valid offer or not
    offer = peek("#offer")
    if not isValid(offer):
      add("<button class=\"btn btn-lg btn-danger\" id=\"warningBtn\">Please "
        "provide a valid input</button><br><br>", "#warning")
      offer = -1

  results = mod.utilities.grabInfo(subj_id)["practice_results"]
  results[practice_id] = offer

  info = take({"tag": "userInfo", "user": subj_id})
  info["practice_results"] = results
  put(info)

  finished = take({"tag": "practice" + str(practice_id + 1) + "Finished"})
  finished["users"].append(subj_id)
  finished["num"] += 1
  put(finished)

def waitingResults(subj_id, me, practice_id):
  let("")
  mod.utilities.updateStage(subj_id, "Finished practice " + str(practice_id + 1))
  add(open("pages/subject/practice_waiting.html"))
  let(str(practice_id + 1), "#practiceItem")
  advance = take({"advance": True, "stage": "waitingPracResults" + str(practice_id + 1)})
  put(advance)

def results(subj_id, me, practice_id):
  let("")
  mod.utilities.updateStage(subj_id, "Practice " + str(practice_id + 1) + " results")
  add(open("pages/subject/practice_results.html"))
  clientResult = take({"tag": "practice_results" + str(practice_id), "user": subj_id})
  put(clientResult)

  let("You <b>" + clientResult["won"] + "</b> the bid to <b>" + str(practice_items[practice_id]) + "</b><span id=\"won\"></span>.", "#results")
  if clientResult["won"] == "won":
    let(" for a price of $<b>" + str(clientResult["offer"]) +"</b>", "#won")
  take({"tag": "click", "client": me, "id": "continue"})

def waitingPractice2(subj_id, me):
  let("")
  mod.utilities.updateStage(subj_id, "Waiting for practice 2")
  add(open("pages/subject/practice_btwnparts.html"))

  # Wait for the advance token and update position
  advance = take({"advance": True, "stage": "waitingPractice2"})
  put(advance)
  mod.utilities.setPosition(subj_id, "practiceInput2")

def input1(subj_id, me):
  input(subj_id, me, 0)
  mod.utilities.setPosition(subj_id, "waitingPracticeResults1")

def input2(subj_id, me):
  input(subj_id, me, 1)
  mod.utilities.setPosition(subj_id, "waitingPracticeResults2")

def waitingResults1(subj_id, me):
  waitingResults(subj_id, me, 0)
  mod.utilities.setPosition(subj_id, "practiceResults1")

def waitingResults2(subj_id, me):
  waitingResults(subj_id, me, 1)
  mod.utilities.setPosition(subj_id, "practiceResults2")

def results1(subj_id, me):
  results(subj_id, me, 0)
  mod.utilities.setPosition(subj_id, "waitingPractice2")

def results2(subj_id, me):
  results(subj_id, me, 1)
  mod.utilities.setPosition(subj_id, "partBInstructions")

