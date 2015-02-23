from willow.willow import *

def start(me, subj_id, waters):
  i = 0
  while i < len(waters):
    add(open("pages/subject/exp_part1.html"))
    let(waters[i], "#waterID")
    show("#validInput")
    take({"tag": "click", "id": "submit", "client": me})
    offer = peek("#offer")

    add("<p>" + str(subj_id) + " has offered $<b>" + str(offer) + "</b> to drink <b>" + waters[i] + "</b>.</p>", "#experimentData", clients=0)
    let("")
    i += 1

