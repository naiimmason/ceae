from willow.willow import *
import numpy as np
buckets = [5, 10, 15, 20, 25, 30, 5000]

def calculate(me):
  clientsFinished = take({"tag": "numFinishedStage1"})
  put(clientsFinished)
  numClientsFinished = int(clientsFinished["num"])
  clientData = []
  for client in clientsFinished["clients"]:
    clientData.append(take({"client": client, "tag": "clientData1"}))

  water1_values = []
  water2_values = []
  water3_values = []
  median_values = []

  for client in clientData:
    water1_values.append(float(client["results"][0]))
    water2_values.append(float(client["results"][1]))
    water3_values.append(float(client["results"][2]))

  print water1_values
  print water2_values
  print water3_values

  water1_median = np.median(water1_values)
  water2_median = np.median(water2_values)
  water3_median = np.median(water3_values)

  for value in water1_values:
    if value == water1_median:
      water1_median = min(water1_values)
      break;

  for value in water2_values:
    if value == water2_median:
      water2_median = min(water2_values)
      break;

  for value in water3_values:
    if value == water3_median:
      water3_median = min(water3_values)
      break;


  median_values.append(water1_median)
  median_values.append(water2_median)
  median_values.append(water3_median)

  tallies_water1 = [0, 0, 0, 0, 0, 0, 0]
  tallies_water2 = [0, 0, 0, 0, 0, 0, 0]
  tallies_water3 = [0, 0, 0, 0, 0, 0, 0]
  
  for value in water1_values:
    i = 0
    while i <= len(buckets):
      if value <= buckets[i]:
        tallies_water1[i] += 1
        i = len(buckets) + 1
      i += 1

  for value in water2_values:
    i = 0
    while i <= len(buckets):
      if value <= buckets[i]:
        tallies_water2[i] += 1
        i = len(buckets) + 1
      i += 1

  for value in water3_values:
    i = 0
    while i <= len(buckets):
      if value <= buckets[i]:
        tallies_water3[i] += 1
        i = len(buckets) + 1
      i += 1

  all_water = [tallies_water1, tallies_water2, tallies_water3]
  print median_values
  return median_values, all_water
