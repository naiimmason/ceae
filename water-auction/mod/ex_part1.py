from willow.willow import *

def start(me, subj_id, waters):
  results = []
  # Loop through all of the water choices
  i = 0
  while i < len(waters):
    add(open("pages/subject/exp_part1.html"))
    let(waters[i], "#waterID")

    # Wait for the client to submit an offer
    # TODO: Add input checks
    take({"tag": "click", "id": "submit", "client": me})
    offer = peek("#offer")
    results.append(offer)

    # Log to monitor and clear screen
    let("")
    i += 1

  return results

