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
time = datetime.datetime.now().isoformat().replace(':',"-")
data_filepath1 = "log/" + time + "-DATA.csv"
survey_filepath1 = "log/" + time + "-SURVEY.csv"

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

    if me ==0:
        users = {}
        while True:
            msg = take({"tag":"entered"},{"tag":"getClient"})

            #associate an id with a client and add it to the list of valid ids
            if msg["tag"]=="entered":
                users[msg["id"]]=msg["client"]

            #get the client associated with an id
            if msg["tag"]=="getClient":
                if not users.has_key(msg["id"]):
                    put({"tag":"giveClient", "client":0})
                else:
                    put({"tag":"giveClient", "client": users[msg["id"]]})

    else:
        add(open("pages/login.html"))
        subj_id = waitForConsent(me)
        #add id to the list of valid ids
        put({"tag":"entered","id":subj_id,"client":me})

        #start subject specific code
        subject.start(me,subj_id,data_filepath1,survey_filepath1)


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
    valid_name = isValid(subj_id,me)

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
def isValid(name,me):
    if name == "":
        return False

    if me==0:
        if name !="econadmin012":
            return False

    if me!=0 and getClient(name)!=0: #client name exists so it is not valid
        return False

    return True

#all the steps to prepare the subject for a reconnect after clicking the reconnect link
def reconnectPage(me):
    go = True
    let("")
    let(open("pages/reconnect.html"))
    while go:
        tak = take({"tag": "click", "client": me, "id": "reconnect"})
        subj_id = peek("#id-input")
        if getClient(subj_id) != 0:
            go = False
            url = peek("#reconnectUrl")
            poke("href",url+str(getClient(subj_id)),"#reconnectHref")
            let("Click Here To Reconnect","#reconnectHref")
            let("", ".warning")

        else:
            let("", ".warning")
            sleep(.25)
            let("<p>That id has not been used yet.</p>", ".warning")


def getClient(subj_id):
    put({"tag":"getClient","id":subj_id})
    msg = take({"tag":"giveClient"})
    return msg["client"]

run(session)
