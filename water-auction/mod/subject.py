from willow.willow import *
import random as rand
import consent
import ex_part1
import ex_part2
import utilities
import practice

# Grab the users info from the tupple space
def grabInfo(subj_id):
  info = take({"tag": "userInfo", "user": subj_id})
  put(info)
  return info

# Get the position of the subject
def getPosition(subj_id):
  return grabInfo(subj_id)["position"]

# Set the position of the user relative to the experiment and readd to tupple 
# space
def setPosition(subj_id, position):
  info = take({"tag": "userInfo", "user": subj_id})
  info["position"] = position
  put(info)

# Update the stage field on the admin table
def updateStage(subj_id, stage):
  let(str(stage),"#" + str(subj_id) + "STAGE", clients=utilities.findAdmin())

# The main logic that runs the subject's portion of the experiment
def start(me, subj_id, waters, rand_waters, output_path):
  let("")
  temp_waters = grabInfo(subj_id)["pers_rand_waters"]
  results = [] # This is where all data collected will be stored

  # "start" Instruction page
  if(getPosition(subj_id) == "start"):
    # Show first instruction page and wait for them to continue
    add(open("pages/subject/prac_instructions.html"))
    take({"tag": "click", "id": "continue", "client": me})
    let("")

    # Update number of people who are waiting to start
    utilities.increment("numStart", me)
    setPosition(subj_id, "waitingPractice")

  # "waitingPractice" Waiting for practice page
  if(getPosition(subj_id) == "waitingPractice"):
    # Open waiting landing page and wait for advance packet before moving on and
    # updating the numbers
    updateStage(subj_id, "Waiting for practice")
    add(open("pages/subject/landing.html"))
    advance = take({"advance": True, "client": utilities.findAdmin(), "stage": 1})
    put(advance)
    setPosition(subj_id, "practiceInput")

  # "practiceInput" Practice page
  if(getPosition(subj_id) == "practiceInput"):
    practice.start(subj_id)
    
  # "waitingPracticeResults" Waiting for practice results page
  # "practiceResults" The practice round's results
  # "partBInstructions" Part B instructions page
  # "waitingPartB" Part B waiting to start page
  # "partBWater1" Part B water 1 page
  # "partBWater2" Part B water 2 page
  # "partBWater3" Part B water 3 page
  # "waitingPartC" Waiting for part C page
  # "partCWater1" Part c water 1 page
  # "partCWater2" Part c water 2 page
  # "partCWater3" Part c water 3 page
  # "results" Results page
  # "endSurvey" Survey page

  utilities.increment("numStage1", me)
  utilities.decrement("numStart", me)
  updateStage(subj_id, "Stage 1")
  let("")
  setPosition(subj_id, 3)
  # TODO: Loop 3 times and make first two the practice part
  # Run through the two parts of the experiment and store the results
  results += ex_part1.start(me, subj_id, waters, temp_waters)

  # Update numbers of where people are
  utilities.decrement("numStage1", me)
  utilities.increment("numFinishedStage1", me)

  updateStage(subj_id, "Finished Stage 1")
  # Put current data on stack for analysis before moving on
  clientData1 = { "client": me, "tag": "clientData1", "results": results }
  put(clientData1)

  # Open a waiting page and wait for advance packet
  add(open("pages/subject/btwnparts.html"))
  advance = take({"advance": True, "client": utilities.findAdmin(), "stage": 2})
  median_values = advance["median"] # Grab median values from advance packet
  all_water = advance["all_water"]
  put(advance)
  let("")

  # Update the numbers of where people are
  utilities.decrement("numFinishedStage1", me)
  utilities.increment("numStage2", me)

  updateStage(subj_id, "Stage 2")
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
  utilities.decrement("numStage2", me)
  utilities.increment("numFinished", me)

  # Log data
  add("<p><b>" + subj_id + "</b> finished: " + ", ".join(clientData2["results"]) + "</p>", "#experimentData", clients=0)

  updateStage(subj_id, "Finished experiment")
  # Open results page and wait for finish packet
  add(open("pages/subject/results.html"))
  let("<p>Waiting for everyone to finish...</p>", "#results")

  # Wait for the monitor to terminate the experiment
  finish = take({"finish": "true", "client": utilities.findAdmin()})
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
