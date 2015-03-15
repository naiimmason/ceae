from willow.willow import *
import random as rand
import mod_calculatemedian
import utilities

btntexts = {
  "waitingPractice1": "Start Practice 1",
  "waitingPracResults1": "Finish Practice 1",
  "waitingPractice2": "Start Practice 2",
  "waitingPracResults2": "Finish Practice 2",
  "waitingPartB": "Start Part B",
  "waitingPartC1": "Start Part C 1",
  "waitingPartC2": "Start Part C 2",
  "waitingPartC3": "Start Part C 3",
  "waitingResults": "Finish Experiment",
  "finished": "NO MORE STAGES!"
}

positions = [
  "waitingPractice1",
  "waitingPracResults1",
  "waitingPractice2",
  "waitingPracResults2",
  "waitingPartB",
  "waitingPartC1",
  "waitingPartC2",
  "waitingPartC3",
  "waitingResults",
  "finished"
]

chat_time = 30

# Main logic thread for the admin
def start(me, waters):
  let("")
  median_values_final = []

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
  num = 0
  i = 0
  while i < len(positions):
    if stage["stage"] == positions[i]:
      position = i
    i += 1

  finish = False
  while not finish:
    action = take({"tag": "click", "id": "advance", "client": me},
                  {"tag": "click", "id": "communication", "client": me},
                  {"tag": "click", "id": "updateMaxPayout", "client": me})

    if action["id"] == "advance":
      position += 1
      poke("value", str(position), "#advance")
      stage = take({"tag": "currentStage"})
      stage["stage"] = positions[position]
      if positions[position] == "finished":
        finish = True

      put(stage)
      advance = {"advance": True, "client": me, "stage": positions[position-1]}

      if positions[position-1] == "waitingPracResults1"  or positions[position-1] == "waitingPracResults2":
        number = 1 
        if positions[position-1] == "waitingPracResults2":
          number = 2

        max_payout = take({"tag": "maxPayout"})
        maxPayout = max_payout["amount"]
        put(max_payout) 

        prac1Data = []
        orderedResults = []
        finishers1 = take({"tag": "practice" + str(number) + "Finished"})
        put(finishers1)

        for user in finishers1["users"]:
          prac1UserData = take({"tag": "userInfo", "user": user})
          put(prac1UserData)
          prac1Data.append({"user": user, "offer": prac1UserData["practice_results"][number-1]})
          orderedResults.append(prac1UserData["practice_results"][number-1])

        winners = []
        winner = -1
        minimum = maxPayout
        nextHighest = maxPayout

        # go through each offer check against minimum and next highest
        for user in prac1Data:
          offer = float(user["offer"])
          user_id = user["user"]

          # if new lowest set nexthighest to minimum and minimum to the new offer 
          # and make sure to rest the nextHighest to the previous minimum
          if offer < minimum:
            winners[:] = []
            nextHighest = minimum
            minimum = offer
            winners.append(user_id)

          # add more than one winner
          elif offer == minimum:
            winners.append(user["user"])
            nextHighest = minimum

          # if the offer is less than the next highest set the next highest
          elif offer < nextHighest:
            nextHighest = offer

        if minimum > maxPayout:
          winners = []
          winner = -1

        orderedResults.sort()
        orderedResults = map(str, orderedResults)
        winners = map(str, winners)
        add("<h4>Practice " + str(number) + "</h4>", "#experimentData")
        add("<p> Winner: " + ", ".join(winners) + "</p>", "#experimentData")
        add("<p> Minimum Amt: $" + str(minimum) + "</p>", "#experimentData")
        add("<p> Payout: $" + str(nextHighest) + "</p>", "#experimentData")
        add("<p> Max Payout: " + str(maxPayout) + "</p>", "#experimentData")

        # if more than 1 winner choose random
        if len(winners) > 1:
          winner = winners[rand.randint(0, len(winners) - 1)]
        else:
          if len(winners) > 0:
            winner = winners[0]

        add("<p> Real Winner: " + str(winner) + "</p>", "#experimentData")
        add("<p>All bids: " + ", ".join(orderedResults) + "</p>", "#experimentData")
        add("<hr>", "#experimentData")

        for user in prac1Data:
          clientPracResult = { "user": user["user"], "won": "did not win", "tag": "practice_results" + str(number-1) }
          if winner == user["user"]:
            clientPracResult["won"] = "won"
            clientPracResult["offer"] = nextHighest

          put(clientPracResult)

      # If moving on to stage 2 perform calculations by grabbing client data 
      # moving on
      if positions[position-1] == "waitingPartC1":
        median_values, all_water = mod_calculatemedian.calculate(me)
        median_values_final = median_values
        advance["median"] = median_values
        advance["all_water"] = all_water

        comm = take({"tag": "communication"})
        put(comm)
        if not comm["communication"]:
          position += 2

      if positions[position] == "waitingResults":
        pop("btn-primary", "#advance")
        push("btn-danger", "#advance")


      # Show advance packet
      put(advance)
      let(btntexts[positions[position]], "#advance")

      if(positions[position-1] == "waitingPartC1" or positions[position-1] == "waitingPartC2" or  positions[position-1] == "waitingPartC3"):
        comm = take({"tag": "communication"})
        put(comm)
        if comm["communication"]:
          for i in range(chat_time):
            sleep(1)
            minutes = int((chat_time - i)/60)
            seconds = int(chat_time-i)%60
            put({"tag": "chatTime" + str(num), "minutes": minutes, "seconds" : seconds, "totSeconds": (chat_time - i)})
          put({"tag": "doneChat" + str(num)})
          num += 1

      
    elif action["id"] == "communication":
      comm = take({"tag": "communication"})
      comm["communication"] = not comm["communication"]
      put(comm)

    elif action["id"] == "updateMaxPayout":
      maxPayout = float(peek("#maxInput"))
        # Update max payout text
      max_payout = take({"tag": "maxPayout"})
      max_payout["amount"] = maxPayout
      put(max_payout)
      let(str(max_payout["amount"]), "#maxPayout")

  # Check out the choice and then depending on the number (btwn 1 and 6) decide 
  # on how to handle client data and gather all data from clients that they have posted in
  choice = int(peek("#resultInput")) - 1 # assume 1-6 thus -1 for array values
  clientsFinished = take({"tag": "numFinished"})
  put(clientsFinished)
  numClientsFinished = int(clientsFinished["num"])
  clientData = []
  for client in clientsFinished["clients"]:
    clientData.append(take({"tag": "clientData2"}))

  advance = take({"advance": True, "stage": "waitingPartC1"})
  put(advance)
  median_values_final = advance["median"]

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

  max_payout = take({"tag": "maxPayout"})
  maxPayout = max_payout["amount"]
  put(max_payout) 

  majority = False
  winners = []
  winner = -1
  minimum = maxPayout + 1
  nextHighest = maxPayout + 1

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

    if nextHighest > maxPayout:
      nextHighest = minimum

    if minimum > maxPayout:
      winners = []
      winner = -1

    majority = False
    winners = map(str, winners)
    add("<hr>", "#experimentData")
    add("<h4>Experiment Finished</h4>", "#experimentData")
    add("<p> Winner: " + ", ".join(winners) + "</p>", "#experimentData")
    add("<p> Minimum Amt: $" + str(minimum) + "</p>", "#experimentData")
    add("<p> Payout: $" + str(nextHighest) + "</p>", "#experimentData")
    add("<p> Max Payout: " + str(maxPayout) + "</p>", "#experimentData")

    # if more than 1 winner choose random
    if len(winners) > 1:
      winner = winners[rand.randint(0, len(winners) - 1)]
    else:
      if len(winners) > 0:
        winner = winners[0]

    add("<p> Real Winner: " + winner + "</p>", "#experimentData")
  elif choice >= 3 and choice <= 5: # If the proctor chose between 4 and 6  
    # compare tally to how many clients finished and check if majority
    if options4_6_tally > numClientsFinished/2:
      majority = True
    add("<p>" + str(majority) + ", " + str(options4_6_tally) + " tally, " + str(numClientsFinished) + " clients, payout of " + str(median_values_final[choice%3]) + " </p>", "#experimentData")

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


