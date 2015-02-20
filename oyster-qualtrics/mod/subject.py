from willow.willow import *
import random as rand

def start(me, out_filepath):
  # Open up intro page and log information
  add(open("pages/index.html"))
  add("<p>Client " + str(me) + " has logged in</p>", "#debuggingData", clients=0)

  # Begin thread logic
  next_page = False
  consent = False
  subj_id = ""

  # Make sure the subject has consented to the experiment and that they have filled in the ID parameter
  while consent == False or subj_id == "" or next_page == False:
    next_page = False

    # Wait for the person to press continue or to press the consent button
    action = take({"tag": "click", "id": "consentSubmit", "client": me},
                  {"tag": "click", "id": "consent", "client": me})

    # check to see which button they pressed and toggle appropriate value
    if action["id"] == "consent":
      consent = not consent
    elif action["id"] == "consentSubmit":
      next_page = True

    # Peek at their subject ID to update it
    subj_id = peek("#idInput")

  # Allow the subject to proceed and clear the page
  add("<p>subject my proceed</p>")
  add("<p>" + str(subj_id) + " has started the experiment</p>", "#experimentData", clients=0)
  let("")

  # Load the first page and wait until they hit continue
  add(open("pages/page1.html")) 
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  # Load the second page and generate random price value for oysters
  add(open("pages/page2.html"))
  quality = "high" # oyster quality
  offer = rand.random()
  if offer < .1:
    offer = 0.0
  elif offer < .2:
    offer = 10.0
  else:
    offer = (((rand.random()*2.0 - 1.0) + (rand.random()*2.0 -1.0) + (rand.random()*2.0-1.0))*1.0+4.5)

  # Format the value and display the value of the element with offer id
  offer = "%.2f" % offer
  let(offer, "#offer")

  # Wait for an answer to be submitted by the client
  answer = take({"tag": "click", "id": "yes", "client":me},
    {"tag": "click", "id": "no", "client":me})
  # Display answer to the monitor
  add("<p>" + str(subj_id) + " has said <b>" + answer["id"] + "</b> to an offer of <b>$" + str(offer) + "</b></p>", "#experimentData", clients=0)

  # Output the answer and data to the relavent database file
  output_file = open(out_filepath, "a")
  output_file.write(str(me) + ", " + str(subj_id) + ", " + quality + ", " + str(offer) + ", " + answer["id"] + "\n")
  output_file.close()

  let("")
  add("<h1>Thanks for taking the survey!</h1>")
