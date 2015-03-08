from willow.willow import *
import random as rand
import matplotlib.pyplot as plt
import mod_calculatemedian
import utilities

btntexts = {
  "waitingPractice1": "Start Practice 1",
  "waitingPracResults1": "Finish Practice 1",
  "waitingPractice2": "Start Practice 2",
  "waitingPracResults2": "Finish Practice 2",
  "waitingPartB": "Start Part B",
  "waitingPartC": "Start Part C",
  "waitingResults": "Finish Experiment"
}

positions = [
  "waitingPractice1",
  "waitingPracResults1",
  "waitingPractice2",
  "waitingPracResults2",
  "waitingPartB",
  "waitingPartC",
  "waitingResults"
]

# Main logic thread for the admin
def start(me, waters):
  let("")

  # Open up the display and then wait until the proctor wants to finish the 
  # experiment
  add(open("pages/monitor/monitor.html"))
  action = {"id": "not started"}

  # Update the table if not made yet
  totalUsers = take({"tag": "totalSubjects"})
  put(totalUsers)
  for user in totalUsers["users"]:
    utilities.addUserRow(user)

  # Update the button text
  stage = take({"tag": "currentStage"})
  put(stage)
  let(btntexts[stage["stage"]], "#advance")
  poke("value", stage["stage"], "#advance")

  # Update max payout text
  max_payout = take({"tag": "maxPayout"})
  put(max_payout)
  let(str(max_payout["amount"]), "#maxPayout")

  position = 0
  i = 0
  while i < len(positions):
    if stage["stage"] == positions[i]:
      position = i
    i += 1


  while action["id"] != "finish":
    action = take({"tag": "click", "id": "finish", "client": me}, 
                  {"tag": "click", "id": "advance", "client": me},
                  {"tag": "click", "id": "communication", "client": me})

    if action["id"] == "advance":
      position += 1
      poke("value", str(position), "#advance")
      stage = take({"tag": "currentStage"})
      stage["stage"] = positions[position]
      put(stage)
      advance = {"advance": True, "client": me, "stage": position}

      # If moving on to stage 2 perform calculations by grabbing client data 
      # moving on
      if position == 3:
        median_values, all_water = mod_calculatemedian.calculate(me)
        advance["median"] = median_values
        advance["all_water"] = all_water
      
      # Show advance packet
      put(advance)
      let(btntexts[positions[position]], "#advance")
      
    elif action["id"] == "communication":
      comm = take({"tag": "communication"})
      comm["communication"] = not comm["communication"]
      put(comm)

  # Check out the choice and then depending on the number (btwn 1 and 6) decide 
  # on how to handle client data and gather all data from clients that they have posted in
  choice = int(peek("#resultInput")) - 1 # assume 1-6 thus -1 for array values
  clientsFinished = take({"tag": "numFinished"})
  put(clientsFinished)
  numClientsFinished = int(clientsFinished["num"])
  clientData = []
  for client in clientsFinished["clients"]:
    clientData.append(take({"tag": "clientData2"}))

  # define variable
  options4_6_tally = 0
  options1_3_offers = []

  # go through each client's data
  for client in clientData:
    # what did the client say for the one option we chose?
    client_choice = client["results"][choice]

    # depending on our choice add to the desired data set
    if choice >= 0 and choice <=2:
      options1_3_offers.append({"offer": float(client_choice), "user": client["user"]})
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
      client_id = client["user"]

      # if new lowest set nexthighest to minimum and minimum to the new offer 
      # and make sure to rest the nextHighest to the previous minimum
      if offer < minimum:
        winners[:] = []
        nextHighest = minimum
        minimum = offer
        winners.append(client_id)

      # add more than one winner
      elif offer == minimum:
        winners.append(client["user"])
        nextHighest = minimum

      # if the offer is less than the next highest set the next highest
      elif offer < nextHighest:
        nextHighest = offer

    majority = False
    winners = map(str, winners)
    add("<p> Winner: " + ", ".join(winners) + "</p>", "#experimentData")
    add("<p> Minimum Amt: $" + str(minimum) + "</p>", "#experimentData")
    add("<p> Payout: $" + str(nextHighest) + "</p>", "#experimentData")

    # if more than 1 winner choose random
    if len(winners) > 1:
      winner = winners[rand.randint(0, len(winners) - 1)]
    else:
      winner = winners[0]

    add("<p> Real Winner: " + winner + "</p>", "#experimentData")
  elif choice >= 3 and choice <= 5: # If the proctor chose between 4 and 6  
    # compare tally to how many clients finished and check if majority
    if options4_6_tally > numClientsFinished/2:
      majority = True
    add("<p>" + str(majority) + ", " + str(options4_6_tally) + " tally, " + str(numClientsFinished) + " clients </p>", "#experimentData")

  # Loop through each client and craft a result dictionary for them to fetch and
  # display results
  for client in clientData:
    clientResult = {}

    if choice >=0 and choice <=2:
      clientResult = {"client": client["client"], "payout": "none", "winner": False, "tag": "clientResult", "type": "payout", "water": choice, "user": client["user"]}
      if client["user"] == winner:
        clientResult["payout"] = nextHighest
        clientResult["winner"] = True
    elif choice >= 3 and choice <= 5:
      clientResult = {"client": client["client"], "majority": majority, "for": options4_6_tally, "total": numClientsFinished, "tag": "clientResult", "type": "majority", "water": choice%3, "user": client["user"]}

    put(clientResult)

  put({"finish": "true", "client": me, "choice": choice})


