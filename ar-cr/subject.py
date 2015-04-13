from willow.willow import *
from scipy.stats import norm
import reconnect
import random as rand

# Treatments and everything defined at the top for easy access
mean = 8
std_dev = 1.50
num_questions = 6
bank = 15.0

ar_treatments = [
  "10",
  "20",
  "11",
  "9",
  "1",
  "0"
]

cr_treatments = [
  "100",
  "200",
  "101",
  "99",
  "1",
  "0"
]

phys_treatments = [
  "submerge your hand in water",
  "breathe in water vapors",
  "drink 2 oz. of water"
]

def start(me, subj_id, data_filepath1, survey_filepath1):
  let("")
  add(open("pages/subject.html"))

  # Show the instructions screen parts 1 and parts 2
  if reconnect.getPosition(subj_id) == "start":
    pop("hidden", ".instructions")
    take({"tag": "click", "id": "continue", "client": me})
    push("hidden", ".instructions")
    reconnect.updatePosition(subj_id, "instructions2")

  if reconnect.getPosition(subj_id) == "instructions2":
    pop("hidden", ".instructions2")
    take({"tag": "click", "id": "continue", "client": me})
    push("hidden", ".instructions2")

    # Determine random order for treatments
    phys_treatment = [];
    chem_treatment = [];
    conc_treatment = [];
    price_treatment = [];

    # For each questions choose randomly either chromium or arsenic and choose
    # a random choice from the specified concentrations along with a random
    # price and physical treatment
    for i in range(num_questions):
      if rand.random() < .5:
        chem_treatment.append("Arsenic")
        conc_treatment.append(rand.choice(ar_treatments))
      else:
        conc_treatment.append(rand.choice(cr_treatments))
        chem_treatment.append("Chromium-3")
      phys_treatment.append(rand.choice(phys_treatments))
      price_treatment.append(gen_price())

    # Add all of the values to the subject's dictionary for reconnect purposes
    # and continuities sake
    reconnect.updateValue(subj_id, "phys_treatment", phys_treatment)
    reconnect.updateValue(subj_id, "chem_treatment", chem_treatment)
    reconnect.updateValue(subj_id, "conc_treatment", conc_treatment)
    reconnect.updateValue(subj_id, "price_treatment", price_treatment)
    reconnect.updatePosition(subj_id, "experiment")

  # The meat of the experiment is done here
  if reconnect.getPosition(subj_id) == "experiment":
    pop("hidden", ".experiment")

    # Grab all of the treatment options from the subject's dictionary
    chem_treatment = reconnect.grabValue(subj_id, "chem_treatment")
    conc_treatment = reconnect.grabValue(subj_id, "conc_treatment")
    price_treatment = reconnect.grabValue(subj_id, "price_treatment")
    phys_treatment = reconnect.grabValue(subj_id, "phys_treatment")

    # Create the questions and add to the HTML
    for i in range(num_questions):
      add("<p>Choice " + str(i+1) + ":</p>" +
          "<p>Are you willing to " + phys_treatment[i] +" contianing " 
          + chem_treatment[i] + " at a concentration of " + 
          conc_treatment[i] + " ppb for $" + str("{0:.2f}".format(price_treatment[i])) 
          + "?</p>" +
          "<div class=\"center\"><div class=\"half\"><input type=\"radio\" name=\"question" + str(i) 
          + "\" value=\"Yes\"> <label class=\"yesnolabel\">YES</label></div>" +
          "<div class=\"half\"><input type=\"radio\" name=\"question" + str(i) 
          + "\" value=\"No\"> <label class=\"yesnolabel\">No</label></div></div>",
          ".experimentqs")
      add("<hr>", ".experimentqs")


    take({"tag": "click", "id": "submit", "client": me})

    # Grab all of their choices from the html that is hidden
    # Make sure that the grab values function actually puts values in the
    # correct spot in the html
    choices = []
    for i in range(num_questions):
      choices.append(peek("#question" + str(i) + "-sel"))

    reconnect.updateValue(subj_id, "selections", choices)
    reconnect.updatePosition(subj_id, "dice_roll")
    push("hidden", ".experiment")

  if reconnect.getPosition(subj_id) == "dice_roll":
    pop("hidden", ".dice-roll")

    take({"tag": "click", "client": me, "id": "dice-button"})
    poke("value", "stop", "#dice-button", )
    
    # Keep rolling the dice until the subject is satisfied
    let("Stop", "#dice-button")
    choice = -1
    stop = False
    while not stop:
      sleep(.02)
      choice = dice_number(num_questions)
      action = grab({"tag": "click", "client": me, "id": "dice-button"})
      if action != None:
        stop = True

    poke("value", "continue", "#dice-button")
    let("Continue", "#dice-button")

    take({"tag": "click", "client": me, "id": "dice-button"})

    reconnect.updateValue(subj_id, "final_selection", choice)
    reconnect.updatePosition(subj_id, "payout")
    push("hidden", ".dice-roll")

  if reconnect.getPosition(subj_id) == "payout":
    # Grab all nneeded information about the subject to make sure that it is all
    # available and in case of a disconnect issue
    pop("hidden", ".payout")
    choice = reconnect.grabValue(subj_id, "final_selection") - 1
    selections = reconnect.grabValue(subj_id, "selections")
    chem_treatment = reconnect.grabValue(subj_id, "chem_treatment")
    conc_treatment = reconnect.grabValue(subj_id, "conc_treatment")
    price_treatment = reconnect.grabValue(subj_id, "price_treatment")
    phys_treatment = reconnect.grabValue(subj_id, "phys_treatment")

    # What was their choice?
    yesorno = selections[choice]
    gained = 0

    if yesorno == "Yes":
      gained = price_treatment[choice]

    money = gained + bank

    # Add HTML to their their output screen
    add("<p>Are you willing to " + phys_treatment[choice] +" contianing " 
      + chem_treatment[choice] + " at a concentration of " + 
      conc_treatment[choice] + " ppb for $" + str("{0:.2f}".format(price_treatment[choice])) 
      + "?</p>",
      "#selected-option")

    let(choice, "#final_choice")
    let(yesorno, "#subj_final_choice")
    let(str("{0:.2f}".format(gained)), "#gained")
    let(str("{0:.2f}".format(money)), "#money")



# Generate a random oyster price based on a mean of 1.50 and a standard deviation
# of 0.50. Using an inverse normal distribution to determine the price.
def gen_price():
  price = norm.ppf(rand.random(), mean, std_dev)
  if price < 0:
    price = 0
  return price

# Generate a random integer based on a num and update the dice in the html
def dice_number(num):
  newnum = rand.randint(1, num)
  let(str(newnum), "#dice-number")
  poke("value", str(newnum), "#dice-number")
  return newnum