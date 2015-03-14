from willow.willow import *
import random as rand
import utilities

# Go through each 
def start(me, subj_id, waters, temp_waters, median_values, all_water, water_pos, output_path):
  let("")
  utilities.updateStage(subj_id, "Part C water " + str(water_pos + 1))
  print all_water
  results = utilities.grabInfo(subj_id)["results"]

  # Loop through all of the water types
  i = water_pos
  add(open("pages/subject/exp_part2.html"))
  let(temp_waters[i], "#waterID")

  # Pick a random price and then wait for an answer from the client
  price = -1

  # Add results to list and log to monitor
  j = 0
  while j < len(waters):
    if temp_waters[i] == waters[j]:
      let(median_values[j], "#price")
      graph_values = all_water[j];
      k = 0
      for value in graph_values:
        add("<span id=\"" + str(k) + "\" value=\"" + str(value) + "\" class=\"hidden\"></span>")
        k+=1
    j += 1
  
  add("<canvas class=\"chartFormat\" id=\"barChart" + str(i + 1) + "\" width=\"600\" height=\"300\"></canvas>", "#chartDiv")

  answer = take({"tag": "click", "id": "Yes", "client": me},
                {"tag": "click", "id": "No", "client": me})

  # Add results to list and log to monitor
  j = 0
  while j < len(waters):
    if temp_waters[i] == waters[j]:
      results[j + 3] = answer["id"]
      add(str(answer["id"]), "#" + str(subj_id) + "water" + str(j + 1) + "B",clients=utilities.findAdmin()) 
    j += 1

  info = take({"tag": "userInfo", "user": subj_id})
  info["results"] = results
  put(info)

  if(i == 0):
    utilities.setPosition(subj_id, "partCWater2")
  elif(i == 1):
    utilities.setPosition(subj_id, "partCWater3")
  elif(i == 2):
    utilities.setPosition(subj_id, "results")
    results = utilities.grabInfo(subj_id)["results"]

    # Make clientData dictionary and push on to Stack
    clientData2 = { "client": me, "tag": "clientData2", "results": results, "user": subj_id }
    put(clientData2)
    # Log data
    add("<p><b>" + subj_id + "</b> finished: " + ", ".join(clientData2["results"]) + "</p>", "#experimentData", clients=utilities.findAdmin())

    # Update numbers of where people are
    utilities.decrement("numStage2", me)
    utilities.increment("numFinished", me)
    prac_results = utilities.grabInfo(subj_id)["practice_results"]


    # Output the answer and data to the relavent database file
    output_file = open(output_path, "a")
    output_file.write(str(me) + ", " + str(subj_id) + ", " + str(prac_results[0]) + ", "  + str(prac_results[1]) + ", " + str(results[0]) + ", " + str(results[1]) + ", " + str(results[2]) + ", " + str(results[3]) + ", " + str(results[4]) + ", " + str(results[5]) +  "\n")
    output_file.close()

  return results
