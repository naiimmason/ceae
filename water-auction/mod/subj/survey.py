from willow.willow import *
import mod.utilities

def start(subj_id, me, survey_path):
  mod.utilities.updateStage(subj_id, "Final Survey")
  let("")
  add(open("pages/subject/survey.html"))

  take({"tag": "click", "id": "continue", "client": me})
  peek_values = ["#thirstyValue",
               "#amtWaterDrink",
               "#tap-water-oftenValue",
               "#fil-tap-water-oftenValue",
               "#bot-water-oftenValue", 
               "#qualityConcern",
               "#riskyTapValue",
               "#riskyFilTapValue",
               "#riskyBottleValue",
               "#riskyDrinkWater",
               "#plasticConcernBother",
               "#plasticConcernOffer",
               "#origin",
               "#originother",
               "#gender",
               "#ageValue",
               "#householdValue",
               "#relstatus",
               "#empstatus",
               "#empstatusOther",
               "#race",
               "#edustatus",
               "#edustatusOther",
               "#income",
               "#currentZip",
               "#pastZip",
               "#commentBox"
               ]

               # "#campingValue", 
                #              "#newBother",
  values = []
  for value in peek_values:
    values.append(str(peek(value)))

  write_string = subj_id
  for value in values:
    write_string += ", " + value

  write_string += "\n"
  survey_file = open(survey_path, "a")
  survey_file.write(write_string)
  survey_file.close()
  mod.utilities.setPosition(subj_id, "last page")

def end(subj_id, me):
  let("")
  mod.utilities.updateStage(subj_id, "END")
  add(open("pages/subject/final.html"))
  payout = mod.utilities.grabInfo(subj_id)["payout"]
  let("$" + str("{0:.2f}".format(payout)), "#" + str(subj_id) + "payout", clients=mod.utilities.findAdmin()) 
  let(str("{0:.2f}".format(payout)), "#payout")


