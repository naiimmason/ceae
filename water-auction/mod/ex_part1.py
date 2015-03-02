from willow.willow import *
import random as rand

def start(me, subj_id, waters):
  results = ["-1", "-1", "-1"]
  # Loop through all of the water choices
  i = 0
  temp_waters = rand.sample(waters, len(waters))

  while i < len(waters):
    add(open("pages/subject/exp_part1.html"))
    let(temp_waters[i], "#waterID")

    # Wait for the client to submit an offer
    # TODO: Add input checks
    take({"tag": "click", "id": "submit", "client": me})
    offer = peek("#offer")
    j = 0
    while j < len(waters):
      if temp_waters[i] == waters[j]:
        results[j] = offer  
      j += 1

    # Log to monitor and clear screen
    let("")
    i += 1

  return results

