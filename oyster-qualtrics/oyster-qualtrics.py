from willow.willow import *
import random as rand
import datetime

datetime.datetime.now().isoformat()
out_filepath = "db/data" + datetime.datetime.now().isoformat() + ".csv"

def session(me):
  # Edit document title and open up starting page, index.html
  let("Oyster Experiment", "title")

  # If you are not the monitor
  if me == 0:
    add(open("pages/monitor.html"))
    output_file = open(out_filepath, "w")
    output_file.write("subject number, subject id, quality, offer, accept?\n")
    output_file.close()

  else:
    add(open("pages/index.html"))
    add("<p>Client " + str(me) + " has logged in</p>", "#debuggingData", clients=0)

    # Begin thread logic
    consent = False
    subj_id = ""

    # Make sure the subject has consented to the experiment and that they have filled in the ID parameter
    while consent == False or subj_id == "":
      # Wait for the person to press continue
      take({"tag": "click", "id": "consentSubmit", "client": me})
      # Check to see if they consented
      temp_consent = grab({"tag": "click", "id": "consentYes", "client": me},
        {"tag": "click", "id": "consentNo", "client": me})

      # Peek at their subject ID
      subj_id = peek("#idInput")
      
      # If they pressed yes then change consent to true
      if temp_consent is not None and temp_consent["id"] == "consentYes":
        consent = True

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
    quality = "high"
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

run(session)
