from willow.willow import *
import random as rand
import utilities
import subject

# Checks to see if an input is a valid float number inside of a certain range
def isValid(input):
  try:
    truth = float(input) >= 0.0 and float(input) <= 5000.0
    return truth
  except ValueError:
    return False

def start(me, subj_id, waters, temp_waters):
  results = ["-1", "-1", "-1"]
  # Loop through all of the water choices
  i = 0
  while i < len(waters):
    add(open("pages/subject/exp_part1.html"))
    let(temp_waters[i], "#waterID")

    # Wait for the client to submit an offer
    offer = -1
    while offer == -1:
      take({"tag": "click", "id": "submit", "client": me})

      # Look at the offer and check if it is a valid offer or not
      offer = peek("#offer")
      if not isValid(offer):
        add("<button class=\"btn btn-lg btn-danger\" id=\"warningBtn\">Please "
          "provide a valid input</button><br><br>", "#warning")
        offer = -1

    # Set the corresponding result with the correct water input AKA random to non-random
    j = 0
    while j < len(waters):
      if temp_waters[i] == waters[j]:
        results[j] = offer 
        add("$" + str(offer), "#" + str(subj_id) + "water" + str(j + 1) + "A",clients=utilities.findAdmin()) 
      j += 1

    # Log to monitor and clear screen
    let("")
    i += 1

  return results

