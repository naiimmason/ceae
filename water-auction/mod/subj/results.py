from willow.willow import *
import mod.utilities
def start(subj_id, me, output_path, waters, median_values):
  let("")
  results = mod.utilities.grabInfo(subj_id)["results"]
  
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
    add("<div id=\"chartLegend\" class=\"\"><p>Yes: " + str(clientResult["for"]) + "</p><p>No: " + str(clientResult["total"] - clientResult["for"]) +"</p></div>", "#chartDiv")
    if clientResult["majority"]: 
      resultStmt += "<p>The majority ruled in favor of the entire group drinking " + waters[clientResult["water"]] + " at a price of $" + str("{0:.2f}".format(median_values[clientResult["water"]])) + "."

    else:
      resultStmt += "<p>The majority ruled against the entire group drinking " +waters[clientResult["water"]] + " at a price of $" + str("{0:.2f}".format(median_values[clientResult["water"]])) + "."

    # Hide data in the html
    add("<span class=\"hidden\" id=\"yes\" value=" + str(clientResult["for"]) + "></span>")
    add("<span class=\"hidden\" id=\"no\" value=" + str(clientResult["total"] - clientResult["for"])+ "></span>")

    # Add canvas for chart drawing, this triggers the arrive event which calls the appropriate js
    add("<canvas id=\"majorityChart\" width=\"400\" height=\"400\"></canvas>", "#chartDiv")

    # Check to see if there is a maxpayout
    payoutDict = take({"tag": "maxPayout"})
    payout = payoutDict["amount"]
    put(payoutDict)
    if payout < median_values[clientResult["water"]]:
      add("<p>However, the maximum payout was $" + str("{0:.2f}".format(payout)) + " (sealed envelope amount) and you will not be paid.</p>", "#maxpayoutDiv")
    else:
      userData = take({"tag": "userInfo", "user": subj_id})
      if not userData["paid"]:
        userData["payout"] += median_values[clientResult["water"]]
        userData["paid"] = True
      put(userData)


  elif clientResult["type"] == "payout":
    if clientResult["winner"] == True:
      resultStmt += "<p>You won the bid for drinking " + waters[clientResult["water"]] + " for $" + str("{0:.2f}".format(clientResult["payout"])) + "</p>"

      userData = take({"tag": "userInfo", "user": subj_id})
      if not userData["paid"]:
        userData["payout"] += clientResult["payout"]
        userData["paid"] = True
      put(userData)
    else:
      resultStmt += "<p>You did not win the bid for drinking " + waters[clientResult["water"]] + ".</p>"
  let(resultStmt, "#results")
  let("$" + str(mod.utilities.grabInfo(subj_id)["payout"]), "#" + str(subj_id) + "payout", clients=mod.utilities.findAdmin())

  add("<hr>", "#buttonYo")
  add("<button class=\"btn btn-primary btn-lg\" id=\"continue\">Continue to Final Survey</button>", "#buttonYo")
  take({"tag": "click", "client": me, "id": "continue"})
  mod.utilities.setPosition(subj_id, "survey")
