from willow.willow import *
import consent
import ex_part1
import ex_part2
import mon_updateNum

def start(me):
  add(open("pages/subject/welcome.html"))
  add("<p>Client " + str(me) + " has logged in</p>", "#debuggingData", clients=0)

  subj_id = consent.waitForConsent(me)
  results = []

  # Allow the subject to proceed and clear the page
  add("<p>subject my proceed</p>")
  add("<p>" + str(subj_id) + " has started the experiment</p>", "#experimentData", clients=0)
  
  mon_updateNum.update("numStarted", me)

  let("")

  # Show first instruction page
  add(open("pages/subject/instructions.html"))
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  # The waters to be used for this experiment
  waters = ["spring water", "re-use tap water", "re-use tap water that has gone through ZeroWater filter"]

  # TODO: Loop 3 times and make first two the practice part
  # Run through the two parts of the experiment and store the results
  results += ex_part1.start(me, subj_id, waters)
  results += ex_part2.start(me, subj_id, waters)

  # Make clientData dictionary and push on to Stack
  clientData = { "client": me, "tag": "clientData", "results": results }
  put(clientData)

  mon_updateNum.update("numFinished", me)

  # Log data
  add("<p><b>" + subj_id + "</b> finished: " + ", ".join(clientData["results"]) + "</p>", "#experimentData", clients=0)

  add(open("pages/subject/results.html"))
  let("<p>Waiting for everyone to finish...</p>", "#results")

  # Wait for the monitor to terminate the experiment
  finish = take({"finish": "true", "client": 0})
  put(finish)

  clientResult = take({"client": me, "tag": "clientResult"})

  resultStmt = ""
  if clientResult["type"] == "majority":
    resultStmt += "<p>The majority ruled <b>" + str(clientResult["majority"])
  elif clientResult["type"] == "payout":
    if clientResult["winner"] == True:
      resultStmt += "<p>You <b>won</b> the bid for drinking <b>" + waters[clientResult["water"]] + "</b> for $<b>" + str(clientResult["payout"]) + "</b></p>" 
    else:
      resultStmt += "<p>You did <b>not</b> win the bid for drinking <b>" + waters[clientResult["water"]] + "</b>.</p>"
  let(resultStmt, "#results")
