from willow.willow import *
import mod.utilities
def start(subj_id, me, output_path, waters, median_values):
  let("")
  results = mod.utilities.grabInfo(subj_id)["results"]

  # Update numbers of where people are
  mod.utilities.decrement("numStage2", me)
  mod.utilities.increment("numFinished", me)
  
  mod.utilities.updateStage(subj_id, "Finished experiment")
  # Open results page and wait for finish packet
  add(open("pages/subject/results.html"))
  let("<p>Waiting for everyone to finish...</p>", "#results")

  # Wait for the monitor to terminate the experiment
  finish = take({"finish": "true"})
  put(finish)

  clientResult = take({"user": subj_id, "tag": "clientResult"})
  put(clientResult)

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
