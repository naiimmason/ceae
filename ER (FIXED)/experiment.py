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
time = datetime.datetime.now().isoformat().replace(":","-")
data_filepath1 = "db/" + time + "-DATA.csv"
survey_filepath1 = "db/" + time + "-SURVEY.csv"

data_file = open(data_filepath1, "w")
data_file.write("DATA FILE, Date," + time + "\n")
data_file.write("subject_id, treatment (A = no epa info / B = epa info), Option " \
                + "selected, option 1, option 2, option 3, option 4, option 5, option 6" + "\n")
data_file.close()

survey_file = open(survey_filepath1, "w")
survey_file.write("SURVEY FILE, Date," + time + "\n")
survey_file.write("Subject ID," \
                  + "How thirsty are you right now?, " \
                  + " In the typical week approximately how many glasses (12 oz.) of tap water do you consume?," \
                  + "Tap Water:," \
                  + "Filtered tap Water:," \
                  + "Bottled Water:," \
                  + "Are you concerned about the quality of your drinking water?," \
                  + "Are you concerned about exposing yourself to water in your community through touch?," \
                  + "Are you concerned about exposing yourself to water in your community through inhalations?," \
                  + "Arsenic:," \
                  + "Chromium:," \
                  + "Lead:," \
                  + "Medication:," \
                  + "Nutrients:," \
                  + "Other (please specify)," \
                  + "How risky do you consider drinking tap water?," \
                  + "How risky do you consider filtered tap water?," \
                  + "How risky do you consider bottled water?," \
                  + "Before today have you ever felt like drinking water may be a risk to your health?," \
                  + "Before today have you ever felt like exposing yourself to water through touch may be a risk to your health?," \
                  + "Before today have you ever felt like exposing yourself to water through inhalation may be a risk to your health?," \
                  + "In general how concerned are you about contaminants in your neighborhood?," \
                  + "How concerned are you about sea level rise negatively affecting you?," \
                  + "How concerned are you about sea level rise negatively affecting your community?," \
                  + "How concerned are you about sea level rise negatively affecting the state of Delaware?," \
                  + "How concerned are you about sea level rise negatively affecting the United States?," \
                  + "How concerned are you about sea level negatively affecting places around the world?," \
                  + "How concerned are you about flooding negatively affecting you?," \
                  + "How concerned are you about flooding negatively affecting your community?," \
                  + "How concerned are you about flooding negatively affecting the state of Delaware?," \
                  + "How concerned are you about flooding negatively affecting the United States?," \
                  + "How concerned are you about flooding negatively affecting places around the world?," \
                  + "How much do you know about global warming?," \
                  + "How much do you know about sea level rise?," \
                  + "How much do you know about flooding?," \
                  + "What is your country of origin?," \
                  + "What is your gender?," \
                  + "Do you have children?," \
                  + "If yes how many children live at home?," \
                  + "What are their ages?," \
                  + "What is your age?," \
                  + "Including yourself how many people live in your household?," \
                  + "What is your relationship status?," \
                  + "Employment status: Are you currently...," \
                  + "Housing: Do you rent or own your place of living?," \
                  + "Housing: Do you live in a house or apartment?," \
                  + "What is your race?," \
                  + "What is your highest level of education obtained?," \
                  + "What is your annual household income?," \
                  + "What is the zip code of your current primary residence?," \
                  + "What zip code (or town) did you grow up in?," \
                  + "Other Concern Input 0-9," \
                  + "Other Country of Origin," \
                  + "Other Employment Status," \
                  + "Other Education Level" \
                  + "\n");
survey_file.close()

# This is the default function that is run upon a connection to the Willow
# server. It is named session by convention and the parameter me is an integer
# that increments by 1 for each new connection and is defined by Willow. Show
# the new person the login page and depending on their name do something.
def session(me):
  # Run things that only need to occur upon the first person joining willow
  if me == 0:
    put({"tag": "totalUsers", "users": []})

  add(open("pages/login.html"))
  subj_id = waitForConsent(me)
  let("")

  if subj_id == "econadmin012":
    print("Hi! I'm an admin!")
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
  print(name)
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
