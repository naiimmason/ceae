################################################################################
# Chat Test - Willow
# This is an experimental economics experiment using the Willow library
# developed and distributed by George Mason University. The University of
# Delaware does not hold any rights to Willow and is merely using it to conduct
# reserach under the BSD liscense. Find willow at
# http://econwillow.sourceforge.net/ and find the University of Delaware at
# http://udel.edu
#
# This is simply a test of a chat box inside of Willow for future reference that
# could be potentially useful.
################################################################################

# Import Willow and needed libraries
from willow.willow import *
import datetime
import random as rand
import subject
import reconnect

# Figure out where to store experiment data and write initial files based on
# time of the experiment in order to provide always unique file names.
time = datetime.datetime.now().isoformat().replace(":","-")
data_filepath1 = "db/" + time + "-DATA.csv"
survey_filepath1 = "db/" + time + "-SURVEY.csv"

data_file = open(data_filepath1, "w")
data_file.write("DATA FILE, Date," + time + "\n")
data_file.close()

survey_file = open(survey_filepath1, "w")
survey_file.write("SURVEY FILE, Date," + time + "\n")
survey_file.close()

# This is the default function that is run upon a connection to the Willow
# server. It is named session by convention and the parameter me is an integer
# that increments by 1 for each new connection and is defined by Willow. Show
# the new person the login page and depending on their name do something.
def session(me):
  # Run things that only need to occur upon the first person joining willow
  if me == 0:
    put({"tag": "totalUsers", "users": [], "numsubjs": 0})

  # Show login page and wait for consent or reconnect
  add(open("pages/login.html"))
  subj_id = waitForConsent(me)
  let("")

  # Do something if the person is an administrator
  if subj_id == "econadmin012":
    print "Hi! I'm an admin!"

  # For everyone else
  else:
    reconnect.addUser(subj_id)
    subject.start(me, subj_id, data_filepath1, survey_filepath1)
    users = take({"tag": "totalUsers"})
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
                  {"tag": "click", "id": "continue", "client": me},
                  {"tag": "click", "id": "reconnect", "client": me})

    subj_id = peek("#id-input")
    valid_name = isValid(subj_id)

    # There are three possible choices, reconnecting, consent, or continue, if
    # they continue they must have pressed consent before and if the reconnect
    # they go through a whole new logic scenario.
    if action["id"] == "reconnect":
      reconnectPage(me);

    elif action["id"] == "consent-button":
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

  return str(subj_id)


# Take a name and see if it has been taken by somebody yet. Check to see if the
# name is empty or contains any other things you wish to check for
def isValid(name):
  print name
  if name == "":
    return False

  if reconnect.userExist(name):
    return False

  users = take({"tag": "totalUsers"})
  put(users)
  users = users["users"]
  for user in users:
    if name == user:
      return False
  return True

# Check to see if that user exists and if they do start them, if not tell them
def reconnectPage(me):
  go = True
  let("")
  add(open("pages/reconnect.html"))
  while go:
    take({"tag": "click", "client": me, "id": "reconnect"})
    subj_id = peek("#id-input")
    if reconnect.userExist(subj_id):
      go = False
      subject.start(me, subj_id, data_filepath1, survey_filepath1)
    else:
      let("", ".warning")
      sleep(.25)
      let("<p>That id has not been used yet.</p>", ".warning")

run(session)
