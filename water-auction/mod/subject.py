from willow.willow import *
import random as rand
import consent
import ex_part1
import ex_part2
import mon_updateNum

def start(me, waters, rand_waters, output_path):
  # Open up the welcome page
  add(open("pages/subject/welcome.html"))
  add("<p>Client " + str(me) + " has logged in</p>", "#debuggingData", clients=0)

  # For the person to consent and fill in their name
  subj_id = consent.waitForConsent(me)
  results = [] # This is where all data collected will be stored

  # The waters to be used for this experiment, these are IN ORDER

  # Allow the subject to proceed and clear the page
  add("<p>subject my proceed</p>")
  add("<p>" + str(subj_id) + " has started the experiment</p>", "#experimentData", clients=0)
  
  # Update the total number of subjects
  mon_updateNum.update("totalSubjects", me)
  let("")

  # Show first instruction page and wait for them to continue
  add(open("pages/subject/prac_instructions.html"))
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  # Update number of people who are waiting to start
  mon_updateNum.update("numStart", me)

  # Open waiting landing page and wait for advance packet before moving on and
  # updating the numbers
  add(open("pages/subject/landing.html"))
  advance = take({"advance": True, "client": 0, "stage": 1})
  put(advance)
  mon_updateNum.update("numStage1", me)
  mon_updateNum.decrement("numStart", me)
  let("")

  # TODO: Loop 3 times and make first two the practice part
  # Run through the two parts of the experiment and store the results
  results += ex_part1.start(me, subj_id, waters)

  # Update numbers of where people are
  mon_updateNum.decrement("numStage1", me)
  mon_updateNum.update("numFinishedStage1", me)

  # Put current data on stack for analysis before moving on
  clientData1 = { "client": me, "tag": "clientData1", "results": results }
  put(clientData1)

  # Open a waiting page and wait for advance packet
  add(open("pages/subject/btwnparts.html"))
  advance = take({"advance": True, "client": 0, "stage": 2})
  median_values = advance["median"] # Grab median values from advance packet
  all_water = advance["all_water"]
  put(advance)
  let("")

  # Update the numbers of where people are
  mon_updateNum.decrement("numFinishedStage1", me)
  mon_updateNum.update("numStage2", me)

  # Perform the second part of the experiment
  results += ex_part2.start(me, subj_id, waters, rand_waters, median_values, all_water)

  # Make clientData dictionary and push on to Stack
  clientData2 = { "client": me, "tag": "clientData2", "results": results }
  put(clientData2)

  # Output the answer and data to the relavent database file
  output_file = open(output_path, "a")
  output_file.write(str(me) + ", " + str(subj_id) + ", " + str(results[0]) + ", " + str(results[1]) + ", " + str(results[2]) + ", " + str(results[3]) + ", " + str(results[4]) + ", " + str(results[5]) +  "\n")
  output_file.close()

  # Update numbers of where people are
  mon_updateNum.decrement("numStage2", me)
  mon_updateNum.update("numFinished", me)

  # Log data
  add("<p><b>" + subj_id + "</b> finished: " + ", ".join(clientData2["results"]) + "</p>", "#experimentData", clients=0)

  # Open results page and wait for finish packet
  add(open("pages/subject/results.html"))
  let("<p>Waiting for everyone to finish...</p>", "#results")

  # Wait for the monitor to terminate the experiment
  finish = take({"finish": "true", "client": 0})
  put(finish)

  clientResult = take({"client": me, "tag": "clientResult"})

  resultStmt = ""
  if clientResult["type"] == "majority":
    add("<div id=\"chartLegend\" class=\"\"></div>", "#chartDiv")
    if clientResult["majority"]: 
      resultStmt += "<p>The majority ruled <b>in favor of</b> the entire group drinking <b>" + waters[clientResult["water"]] + "</b> at a price of <b>$" + str(median_values[clientResult["water"]]) + "</b>."
    else:
      resultStmt += "<p>The majority ruled <b>against</b> the entire group drinking <b>" +waters[clientResult["water"]] + "</b> at a price of <b>$" + str(median_values[clientResult["water"]]) + "</b>."

    # Hide data in the html
    add("<span class=\"hidden\" id=\"yes\" value=" + str(clientResult["for"]) + "></span>")
    add("<span class=\"hidden\" id=\"no\" value=" + str(clientResult["total"] - clientResult["for"])+ "></span>")

    # Add canvas for chart drawing, this triggers the arrive event which calls the appropriate js
    add("<canvas id=\"majorityChart\" width=\"400\" height=\"400\"></canvas>", "#chartDiv")


  elif clientResult["type"] == "payout":
    if clientResult["winner"] == True:
      resultStmt += "<p>You <b>won</b> the bid for drinking <b>" + waters[clientResult["water"]] + "</b> for $<b>" + str(clientResult["payout"]) + "</b></p>" 
    else:
      resultStmt += "<p>You did <b>not</b> win the bid for drinking <b>" + waters[clientResult["water"]] + "</b>.</p>"
  let(resultStmt, "#results")
