from willow.willow import *
import random as rand

def session(me):
  # Edit document title and open up starting page, index.html
  let("Oyster Experiment", "title")
  add(open("pages/index.html"))

  # Begin thread logic
  consent = False
  subj_id = ""

  # Make sure the subject has consented to the experiment and that they have filled in the ID parameter
  while consent == False or subj_id == "":
    # Wait for the person to press continue
    take({"tag": "click", "id": "consentSubmit", "client": me})
    # Check to see if they consented
    temp_consent = grab({"tag": "click", "id": "consentYes", "client": me})

    # Peek at their subject ID
    subj_id = peek("#idInput")
    
    # If they pressed yes then change consent to true
    if temp_consent is not None:
      consent = True

  # Allow the subject to proceed and clear the page
  add("<p>subject my proceed</p>")
  let("")

  # Load the first page and wait until they hit continue
  add(open("pages/page1.html")) 
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  # Load the second page and generate random price value for oysters
  add(open("pages/page2.html"))
  randNum = rand.random()
  if randNum < .1:
    randNum = 0.0
  elif randNum < .2:
    randNum = 10.0
  else:
    randNum = (((rand.random()*2.0 - 1.0) + (rand.random()*2.0 -1.0) + (rand.random()*2.0-1.0))*1.0+4.5)

  randNum = "%.2f" % randNum
  let(randNum, "#test-output")

run(session)
