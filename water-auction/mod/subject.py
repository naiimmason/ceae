from willow.willow import *
import consent
import ex_part1
import ex_part2
import mon_updateNum

def start(me):
  add(open("pages/subject/welcome.html"))
  add("<p>Client " + str(me) + " has logged in</p>", "#debuggingData", clients=0)

  subj_id = consent.waitForConsent(me)

  # Allow the subject to proceed and clear the page
  add("<p>subject my proceed</p>")
  add("<p>" + str(subj_id) + " has started the experiment</p>", "#experimentData", clients=0)
  
  mon_updateNum.update("numStarted")

  let("")

  # Show first instruction page
  add(open("pages/subject/instructions.html"))
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  # The waters to be used for this experiment
  waters = ["spring water", "re-use tap water", "re-use tap water that has gone through ZeroWater filter"]

  # TODO: Loop 3 times and make first two the practice part
  # Run through the two parts of the experiment
  ex_part1.start(me, subj_id, waters)
  ex_part2.start(me, subj_id, waters)

  mon_updateNum.update("numFinished")

  add("<h1>Waiting for proctor</h1>")
  
  finish = take({"finish": "true", "client": 0})
  put(finish)

  add("<h1>The experiment has finished</h1>")
