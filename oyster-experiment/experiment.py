################################################################################
# Oyster Experiment - Willow
# This is an experimental economics experiment using the Willow library
# developed and distributed by George Mason University. The University of
# Delaware does not hold any rights to Willow and is merely using it to conduct
# reserach under the BSD liscense. Find willow at 
# http://econwillow.sourceforge.net/ and find the University of Delaware at 
# http://udel.edu 
#
# This experiment gauges peoples' interests in oyster quality and how willing 
# they are to purchase oysters at certain prices. This program simply asks them
# how many osyters they want, provides 6 semi-random price per oyster, and then 
# asks if they would be willing to buy X amount of oysters at each price. 
#
# This experiment will be a single page experiment due to the its short and
# simple nature. There doesn't need to be any communication between participants
# and being able to see the whole experiment unfold will be beneficial for the
# subject
################################################################################

# Import Willow and needed libraries
from willow.willow import * 
import datetime
import random as rand
import subject

# Figure out where to store experiment data and write initial files based on
# time of the experiment in order to provide always unique file names.
time = datetime.datetime.now().isoformat()
data_filepath = "db/oyster-" + time + "-DATA.csv"
survey_filepath = "db/oyster-" + time + "-SURVEY.csv" 

# Store the header rows in the data and survey files in order to initialize them
data_file = open(data_filepath, "w")
data_file.write("Date," + time + "\n")
data_file.write("subject, number of oysters, option 1, option 2, option 3, " +
  "option 4, option 5, option 6, Yes To, No To\n")
data_file.close()

survey_file = open(survey_filepath, "w")
survey_file.write("Date," + time + "\n")
survey_file.write("subject\n")
survey_file.close()

# This is the default function that is run upon a connection to the Willow
# server. It is named session by convention and the parameter me is an integer
# that increments by 1 for each new connection and is defined by Willow. Show
# the new person the login page and depending on their name do something.
def session(me):
  # Run things that only need to occur upon the first person joining willow
  if me == 0:
    put({"tag": "users", "users": []})

  let("Oyster Experiment", "title")

  add(open("pages/login.html"))
  subj_id = waitForConsent(me)
  let("")

  if subj_id == "econadmin012":
    print "Hi! I'm an admin!"
  else:
    subject.start(me, subj_id)
    users = take({"tag": "users"})
    users["users"].append(subj_id)
    put(users)

# This function waits for a person on the login page to consent and provide a 
# valid participant id in order to continue.
def waitForConsent(me):
  # These are the three values that have to be true before allowing a person to
  # continue
  next_page = False
  consent = False
  valid_name = False

  subj_id = ""
  while not next_page or not consent or not valid_name:
    next_page = False

    # Wait for the person to take an action and then update the boolean values
    # accordingly
    action = take({"tag": "click", "id": "consent-button", "client": me},
                  {"tag": "click", "id": "continue", "client": me})

    subj_id = peek("#id-input")
    valid_name = isValid(subj_id)

    if action["id"] == "consent-button":
      consent = not consent

    elif action["id"] == "continue":
      next_page = True

      # Add warning if some things are not true
      if not valid_name:
        let("", ".warning")
        sleep(.25)
        let("<p>Please provide a valid participant id.</p>", ".warning")
      elif not consent:
        let("", ".warning")
        sleep(.25)
        let("<p>You must consent before continuing.</p>", ".warning")

  return subj_id


# Take a name and see if it has been taken by somebody yet. Check to see if the
# name is empty or contains any other things you wish to check for
def isValid(name):
  print name
  if name == "":
    return False

  users = take({"tag": "users"})
  put(users)
  users = users["users"]
  for user in users:
    if name == user:
      return False
  return True

run(session)
