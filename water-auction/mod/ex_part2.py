from willow.willow import *
import random as rand

def start(me, subj_id, waters):
  i = 0
  while i < len(waters):
    add(open("pages/subject/exp_part2.html"))
    let(waters[i], "#waterID")
    price = rand.randint(1, 10)
    let(price, "#price")
    answer = take({"tag": "click", "id": "Yes", "client": me},
                  {"tag": "click", "id": "No", "client": me})
    add("<p>" + str(subj_id) + " has said <b>" + answer["id"] + "</b> to the group drinking <b>" + waters[i] + "</b> for the price of <b>$" + str(price) + "</b>.</p>", "#experimentData", clients=0)
    let("")
    i += 1
