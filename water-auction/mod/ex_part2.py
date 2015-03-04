from willow.willow import *
import random as rand

# Go through each 
def start(me, subj_id, waters, temp_waters, median_values, all_water):
  print all_water
  results = ["null", "null", "null"]

  # Loop through all of the water types
  i = 0
  while i < len(waters):
    add(open("pages/subject/exp_part2.html"))
    let(temp_waters[i], "#waterID")

    # Pick a random price and then wait for an answer from the client
    price = rand.randint(1, 10)
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

    add("<canvas id=\"barChart" + str(i + 1) + "\" width=\"600\" height=\"400\"></canvas>", "#chartDiv")

    answer = take({"tag": "click", "id": "Yes", "client": me},
                  {"tag": "click", "id": "No", "client": me})

    # Add results to list and log to monitor
    j = 0
    while j < len(waters):
      if temp_waters[i] == waters[j]:
        results[j] = answer["id"]
      j += 1
    let("")
    i += 1

  return results
