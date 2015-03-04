from willow.willow import *
import random as rand
import matplotlib.pyplot as plt
import mod_calculatemedian

def start(me, waters, output_path):
  # Initialize the output file
  output_file = open(output_path, "w")
  output_file.write("subject info,,Part A,,,Part B,,,\n")
  output_file.write("subject number, subject id, " + waters[0] +", " + waters[1] + ", " + waters[2]+ ", " + waters[0] +", " + waters[1] + ", " + waters[2] +  "\n")
  output_file.close()

  # Put inital dictionaries on to the stack
  put({"tag": "totalSubjects", "num": 0, "clients": []})
  put({"tag": "numStart", "num": 0, "clients": []})
  put({"tag": "numStage1", "num": 0, "clients": []})
  put({"tag": "numFinishedStage1", "num": 0, "clients": []})
  put({"tag": "numStage2", "num": 0, "clients": []})
  put({"tag": "numFinished", "num": 0, "clients": []})

  # Open up the display and then wait until the proctor wants to finish the 
  # experiment
  add(open("pages/monitor/monitor.html"))
  action = {"id": "not started"}

  position = 0
  while action["id"] != "finish":
    action = take({"tag": "click", "id": "finish", "client": me}, 
                  {"tag": "click", "id": "advance", "client": me})

    if action["id"] == "advance":
      position += 1
      poke("value", str(position), "#advance")
      advance = {"advance": True, "client": me, "stage": position}

      # If moving on to stage 2 perform calculations by grabbing client data 
      # moving on
      if position == 2:
        median_values, all_water = mod_calculatemedian.calculate(me)
        advance["median"] = median_values
        advance["all_water"] = all_water
      
      # Show advance packet
      put(advance)
      let("Advance to Stage " + str(position + 1), "#advance")

  # Check out the choice and then depending on the number (btwn 1 and 6) decide 
  # on how to handle client data and gather all data from clients that they have posted in
  choice = int(peek("#resultInput")) - 1 # assume 1-6 thus -1 for array values
  clientsFinished = take({"tag": "numFinished"})
  numClientsFinished = int(clientsFinished["num"])
  clientData = []
  for client in clientsFinished["clients"]:
    clientData.append(take({"client": client, "tag": "clientData2"}))

  # define variable
  options4_6_tally = 0
  options1_3_offers = []

  # go through each client's data
  for client in clientData:
    # what did the client say for the one option we chose?
    client_choice = client["results"][choice]

    # depending on our choice add to the desired data set
    if choice >= 0 and choice <=2:
      options1_3_offers.append({"offer": float(client_choice), "client": client["client"]})
    elif choice >= 3 and choice <= 5:
      if client_choice == "Yes":
        options4_6_tally += 1

  majority = False
  winners = []
  winner = -1
  minimum = 10000000000000
  nextHighest = minimum + 1

  # Analyze the data
  if choice >=0 and choice <=2:
    # Set minimum and next highest to absurd numbers

    # go through each offer check against minimum and next highest
    for client in options1_3_offers:
      offer = client["offer"]
      client_id = client["client"]

      # if new lowest set nexthighest to minimum and minimum to the new offer 
      # and make sure to rest the nextHighest to the previous minimum
      if offer < minimum:
        winners[:] = []
        nextHighest = minimum
        minimum = offer
        winners.append(client_id)

      # add more than one winner
      elif offer == minimum:
        winners.append(client["client"])
        nextHighest = minimum

      # if the offer is less than the next highest set the next highest
      elif offer < nextHighest:
        nextHighest = offer

    majority = False
    winners = map(str, winners)
    add("<p> Winner: " + ", ".join(winners) + "</p>", "#debuggingData")
    add("<p> Minimum Amt: $" + str(minimum) + "</p>", "#debuggingData")
    add("<p> Payout: $" + str(nextHighest) + "</p>", "#debuggingData")

    # if more than 1 winner choose random
    if len(winners) > 1:
      winner = winners[rand.randint(0, len(winners) - 1)]
    else:
      winner = winners[0]

    add("<p> Real Winner: " + winner + "</p>", "#debuggingData")
  elif choice >= 3 and choice <= 5: # If the proctor chose between 4 and 6  
    # compare tally to how many clients finished and check if majority
    if options4_6_tally > numClientsFinished/2:
      majority = True
    add("<p>" + str(majority) + ", " + str(options4_6_tally) + " tally, " + str(numClientsFinished) + " clients </p>", "#debuggingData")

  # Loop through each client and craft a result dictionary for them to fetch and
  # display results
  for client in clientData:
    clientResult = {}

    if choice >=0 and choice <=2:
      clientResult = {"client": client["client"], "payout": "none", "winner": False, "tag": "clientResult", "type": "payout", "water": choice}
      if client["client"] == int(winner):
        clientResult["payout"] = nextHighest
        clientResult["winner"] = True
    elif choice >= 3 and choice <= 5:
      clientResult = {"client": client["client"], "majority": majority, "for": options4_6_tally, "total": numClientsFinished, "tag": "clientResult", "type": "majority", "water": choice%3}

    put(clientResult)

  put({"finish": "true", "client": me, "choice": choice})


