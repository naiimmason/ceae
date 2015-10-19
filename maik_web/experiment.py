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
data_file.close()

survey_file = open(survey_filepath1, "w")
survey_file.write("SURVEY FILE, Date," + time + "\n")
survey_file.close()

# This is the default function that is run upon a connection to the Willow
# server. It is named session by convention and the parameter me is an integer
# that increments by 1 for each new connection and is defined by Willow. Show
# the new person the login page and depending on their name do something.
def session(me):
    let("Maik", "title")
    # Run things that only need to occur upon the first person joining willow
    if me == 0:
        put({"tag": "totalUsers", "users": [], "num": 0})
        add(open("pages/admin.html"))

    else:
        add(open("pages/subject.html"))
        subj_id = me
        let("")
        subject.start(me, subj_id, data_filepath1, survey_filepath1)
        users = take({"tag": "totalUsers"})
        users["num"] = users["num"] + 1
        users["users"].append(subj_id)
        put(users)

run(session)
