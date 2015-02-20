from willow.willow import *
import consent

def start(me):
  add(open("pages/subject/welcome.html"))
  add("<p>Client " + str(me) + " has logged in</p>", "#debuggingData", clients=0)

  subj_id = consent.waitForConsent(me)

  # Allow the subject to proceed and clear the page
  add("<p>subject my proceed</p>")
  add("<p>" + str(subj_id) + " has started the experiment</p>", "#experimentData", clients=0)
  let(me, "#numSubj", clients=0)
  let("")

  # Show first instruction page
  add(open("pages/subject/instructions.html"))
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  # TODO: Loop 3 times and make first two the practice part
  # Run through the first three frames of the experiment

