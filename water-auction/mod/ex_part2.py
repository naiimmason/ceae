from willow.willow import *
import random as rand

# Go through each 
def start(me, subj_id, waters, temp_waters, median_values):
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
      j += 1
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
