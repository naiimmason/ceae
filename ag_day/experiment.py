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
import reconnect

# Figure out where to store experiment data and write initial files based on
# time of the experiment in order to provide always unique file names.
time = datetime.datetime.now().isoformat()
data_filepath1 = "db/NUTRIENTS-oyster-" + time + "-DATA.csv"
survey_filepath1 = "db/NUTRIENTS-oyster-" + time + "-SURVEY.csv"
data_filepath2 = "db/WORDING-oyster-" + time + "-DATA.csv"
survey_filepath2 = "db/WORDING-oyster-" + time + "-SURVEY.csv"

# Store the header rows in the data and survey files in order to initialize them
data_file = open(data_filepath1, "w")
data_file.write("Date," + time + "\n")
data_file.write("subject, treatment, number of oysters, cooked option, chosen option, option 1, option 2, option 3, " +
  "option 4, option 5, option 6, option 7, option 8\n")
data_file.write("example, A, 12, fried, 6, unknown, low, medium, high, unknown, low, medium, high\n")
data_file.write(",,,,,price1,2,3,4,5,6,7,8\n")
data_file.write(",,,,,yes,no,yes,no,yes,no,yes,no\n")
data_file.close()

data_file = open(data_filepath2, "w")
data_file.write("Date," + time + "\n")
data_file.write("subject, treatment, number of oysters, cooked option, chosen option, option 1, option 2, option 3, " +
  "option 4, option 5, option 6\n")
data_file.write("example, A, 12, fried, 6, unknown, low, medium, high, unknown, low\n")
data_file.write(",,,,,price1,2,3,4,5,6\n")
data_file.write(",,,,,yes,no,yes,no,yes,no\n")
data_file.close()

values_to_grab = [
  "age",
  "gender",
  "how often do you consume oysters",
  "are you the primary shopper",
  "what is your profession",
  "other box for profession",
  "political affliation",
  "other box for political affiliatin",
  "household income",
  "highest level of eduation",
  "how often do you go to the beach each year",
  "are you a first time oyster consumer",
  "in a month how often do you eat seafood",
  "in a month how oftedn do you eat at a restaurant",
  "when at a restaurant percent seafood vs other food (0 = all other 100 = all seafood)",
  "how oftend do you eat at home vs a restaurant",
  "are you the primary seafood shopper",
  "how often do you catch your own seafood",
  "how important is location to oyster choice",
  "for oysters from Delaware Bay I would...",
  "for oysters from Delaware Inland bays I would...",
  "how do you usually prepare your oysters",
  "other box for usual oyster prep",
  "how important is oyster species (9 = impmortant 0 = not important)",
  "how important is oyster shell size",
  "how important is oyster meat size",
  "how important is oyster appearance",
  "how important is the saltiness of oysters",
  "how important is the smell of oysters",
  "how important is the oyster shell color",
  "how important is the oyster meat color",
  "how important is the oyster harvest location"
]

worded_questions = [
  "<em>Nauti Pilgrim</em> oysters. These are aquacultured oysters.",
  "Oysters from Plymouth Rock, MA. These are aquacultured oysters.",
  "<em>Little Bitches</em> oysters from Chesapeake Bay in VA.",
  "<em>Little Bitches</em> oysters. These are aquacultured oysters.",
  "Oysters from Chesapeake Bay in VA. These are aquacultured oysters.",
  "Oysters from Long Island, NY. These are wild-caught oysters.",
  "<em>Blue Point</em> oysters from Long Island, NY.",
  "<em>Blue Point</em> oysters. These are wild-caught oysters.",
  "<em>Nauti Pilgrim</em> oysters from Plymouth Rock, MA."]

option_names = ",".join(values_to_grab)

survey_file = open(survey_filepath1, "w")
survey_file.write("Date," + time + "\n")
survey_file.write("subject, " + option_names + "\n")
survey_file.close()

survey_file = open(survey_filepath2, "w")
survey_file.write("Date," + time + "\n")
survey_file.write("subject, " + option_names + "\n")
survey_file.close()

# This is the default function that is run upon a connection to the Willow
# server. It is named session by convention and the parameter me is an integer
# that increments by 1 for each new connection and is defined by Willow. Show
# the new person the login page and depending on their name do something.
def session(me):
  # Run things that only need to occur upon the first person joining willow
  if me == 0:
    put({"tag": "new_questions", "qs": worded_questions})
    put({"tag": "totalUsers", "users": []})
    put({"tag": "TREATNUM", "num": 0})

  let("Oyster Experiment", "title")

  add(open("pages/login.html"))
  subj_id = waitForConsent(me)
  let("")

  if subj_id == "econadmin012":
    print "Hi! I'm an admin!"
    let("")
    add(open("pages/monitor.html"))
  else:
    reconnect.addUser(subj_id)
    subject.start(me, subj_id, data_filepath1, data_filepath2, survey_filepath1, survey_filepath2)
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
      subject.start(me, subj_id, data_filepath1, data_filepath2, survey_filepath1, survey_filepath2)
    else:
      let("", ".warning")
      sleep(.25)
      let("<p>That id has not been used yet.</p>", ".warning")

run(session)
