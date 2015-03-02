from willow.willow import *
import numpy as np

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

  median_values.append(np.median(water1_values))
  median_values.append(np.median(water2_values))
  median_values.append(np.median(water3_values))

  return median_values
