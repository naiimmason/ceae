from willow.willow import *
import mod.monitor
import mod.subject
import mod.consent
import mod.utilities
import mod.reconnect
import random as rand
import datetime

# Define static variables that are to be used throughout the program
datetime.datetime.now().isoformat()
waters = ["Penta Ultra Purified water", "re-use tap water", "re-use tap water that has gone through a ZeroWater filter"]
rand_waters = rand.sample(waters, len(waters))
output_path = "db/data" + datetime.datetime.now().isoformat() + ".csv"

# Initialize the output file
output_file = open(output_path, "w")
output_file.write("subject info,,Part A,,,Part B,,,\n")
output_file.write("subject number, subject id, " + waters[0] +", " + waters[1] + ", " + waters[2]+ ", " + waters[0] +", " + waters[1] + ", " + waters[2] +  "\n")
output_file.close()

def session(me):
  if me == 0:
    # Put inital dictionaries on to the stack, do ONLY ON FIRST JOIN
    # Two most important dictionaries used to check IDs
    put({"tag": "totalSubjects", "num": 0, "clients": [], "users": []})
    put({"tag": "activeUsers", "num": 0, "users": []})

    # Quality of life dictionaries that update admin info
    put({"tag": "numStart", "num": 0, "clients": []})
    put({"tag": "numStage1", "num": 0, "clients": []})
    put({"tag": "numFinishedStage1", "num": 0, "clients": []})
    put({"tag": "numStage2", "num": 0, "clients": []})
    put({"tag": "numFinished", "num": 0, "clients": []})
    put({"tag": "communication", "communication": False})
    put({"tag": "maxPayout", "amount": 4999})
    put({"tag": "currentStage", "stage": "waitingPractice1"})

  # Edit page title
  let("Second-Price Auction", "title")

  # Show login page and ask for consent and check to see if they are the admin 
  # or not
  add(open("pages/welcome.html"));
  subj_id = ""
  if me != 0:
    subj_id = str(mod.consent.waitForConsent(me))

  # Check to see if proctor or not
  if subj_id == "econadmin012" or me == 0:
    # Remove the last adminUser and add the new one
    grab({"tag": "adminUser"})
    put({"tag": "adminUser", "clientNum": me})
    mod.monitor.start(me, waters)

  # Reconnect code goes here
  elif subj_id == "reconnect123456789":
    let("")
    add(open("pages/subject/reconnect.html"))
    subj_id = str(mod.reconnect.wait(me))
    mod.subject.start(me, subj_id, waters, rand_waters, output_path)

  # New unique person is added and starts the experiment
  else:
    # Update the total number of subjects and add a unique dictionary for that user 
    mod.utilities.addUser(subj_id, me)
    temp_waters = rand.sample(waters, len(waters))
    put({"tag": "userInfo", "user": subj_id, "results": [-1, -1, -1, -1, -1, -1], 
      "pers_rand_waters": temp_waters, "position": "Start"})
    mod.utilities.addUserRow(subj_id)
    mod.subject.start(me, subj_id, waters, rand_waters, output_path)

run(session)
