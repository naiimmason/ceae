from willow.willow import *
import random as rand

# Go through each 
def start(me, subj_id, waters):
  results = []

  # Loop through all of the water types
  i = 0
  while i < len(waters):
    add(open("pages/subject/exp_part2.html"))
    let(waters[i], "#waterID")

    # Pick a random price and then wait for an answer from the client
    price = rand.randint(1, 10)
    let(price, "#price")
    answer = take({"tag": "click", "id": "Yes", "client": me},
                  {"tag": "click", "id": "No", "client": me})

    # Add results to list and log to monitor
    results.append(answer["id"])
    let("")
    i += 1

  return results
