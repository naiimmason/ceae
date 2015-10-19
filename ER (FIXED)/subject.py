from willow.willow import *
from scipy.stats import norm
import reconnect
import random as rand

# Treatments and everything defined at the top for easy access
num_questions = 6
bank = 15.0
num_survey_qs = 54

ar_treatments = [
  "10",
  "20",
  "7",
  "13",
  "1",
  "0"
]

cr_treatments = [
  "15",
  "30",
  "10.5",
  "1.5",
  "19.5",
  "0"
]

phys_treatments = [
  "submerge your hand in water for ten seconds",
  "inhale three breaths of vapors from water",
  "drink three ounces of water"
]

def start(me, subj_id, data_filepath1, survey_filepath1):
  let("")
  add(open("pages/subject.html"))

  # Show the instructions screen parts 1 and parts 2
  if reconnect.getPosition(subj_id) == "start":
    pop("hidden", ".instructions")
    take({"tag": "click", "id": "continue", "client": me})
    reconnect.updatePosition(subj_id,"instructions2")
    push("hidden", ".instructions")

    # Determine random order for treatments
    phys_treatment = [];
    chem_treatment = [];
    conc_treatment = [];
    price_treatment = [];

    # For each questions choose randomly either lead or arsenic and choose
    # a random choice from the specified concentrations along with a random
    # price and physical treatment
    for i in range(num_questions):
      if rand.random() < .5:
        chem_treatment.append("Arsenic")
        conc_treatment.append(rand.choice(ar_treatments))
      else:
        conc_treatment.append(rand.choice(cr_treatments))
        chem_treatment.append("Lead")
      phys_treatment.append(rand.choice(phys_treatments))
      price_treatment.append(gen_price())

    # Add all of the values to the subject's dictionary for reconnect purposes
    # and continuities sake
    reconnect.updateValue(subj_id, "phys_treatment", phys_treatment)
    reconnect.updateValue(subj_id, "chem_treatment", chem_treatment)
    reconnect.updateValue(subj_id, "conc_treatment", conc_treatment)
    reconnect.updateValue(subj_id, "price_treatment", price_treatment)

    info_type = "A"
    if rand.random() < .5:
      info_type = "B"
    reconnect.updateValue(subj_id, "info_type", info_type)
    reconnect.updatePosition(subj_id, "experiment")

  # The meat of the experiment is done here
  if reconnect.getPosition(subj_id) == "experiment":
    pop("hidden", ".experiment")

    # Grab all of the treatment options from the subject's dictionary
    chem_treatment = reconnect.grabValue(subj_id, "chem_treatment")
    conc_treatment = reconnect.grabValue(subj_id, "conc_treatment")
    price_treatment = reconnect.grabValue(subj_id, "price_treatment")
    phys_treatment = reconnect.grabValue(subj_id, "phys_treatment")
    info_type = reconnect.grabValue(subj_id, "info_type")

    # Create the questions and add to the HTML
    for i in range(num_questions):
      additional_info = ""
      if info_type == "B":
        additional_info = "<p>The United States Environmental Protection Agency (EPA) drinking water standard for "
      if chem_treatment[i] == "Arsenic" and info_type == "B":
        additional_info += " Arsenic is 10 parts per billion (ppb).</p><br>"
      elif chem_treatment[i] == "Lead" and info_type == "B":
        additional_info += " Lead is 15 parts per billion (ppb).</p><br>"

      add(additional_info + "<p>Task " + str(i+1) + ":</p>" +
          "<p>Are you willing to " + phys_treatment[i] +" from an area that, in a published government report, had levels of "
          + chem_treatment[i] + " that were measured at " +
          conc_treatment[i] + " parts per billion (ppb) for $" + str("{0:.2f}".format(price_treatment[i]))
          + "?</p>" +
          "<div class=\"center\"><div class=\"half\"><input type=\"radio\" name=\"question" + str(i)
          + "\" value=\"Yes\"> <label class=\"yesnolabel\">Yes</label></div>" +
          "<div class=\"half\"><input type=\"radio\" name=\"question" + str(i)
          + "\" value=\"No\"> <label class=\"yesnolabel\">No</label></div></div>",
          ".experimentqs")
      add("<hr>", ".experimentqs")

    # Grab all of their choices from the html that is hidden
    # Make sure that the grab values function actually puts values in the
    # correct spot in the html
    cont = True
    choices = []
    while cont:
      choices = []
      take({"tag": "click", "id": "submit", "client": me})
      cont = False
      for i in range(num_questions):
        choices.append(peek("#question" + str(i) + "-sel"))
        if peek("#question" + str(i) + "-sel") == "":
          cont = cont or True
      if cont:
        let("", ".warning")
        sleep(.25)
        add("<p>Please answer all questions</p>", ".warning")
    let("", ".warning")

    reconnect.updateValue(subj_id, "selections", choices)
    reconnect.updatePosition(subj_id, "survey")
    push("hidden", ".experiment")

  if reconnect.getPosition(subj_id) == "survey":
    pop("hidden", ".survey")
    add(open("pages/survey.html"), "#surveyqs")

    take({"tag": "click", "id": "submit", "client": me})
    let("<p>Please make sure you have answered as many questions as possible. You " +
        "will NOT be able to go back.</p>", ".warning")
    take({"tag": "click", "id": "submit", "client": me})
    let("", ".warning")

    answers = []
    for i in range(num_survey_qs):
      answers.append(peek("#surveyq" + str(i) + "-sel"))
    print answers

    # Write everything to a file
    survey_file = open(survey_filepath1, "a")

    survey_line = str(subj_id) + ", " + ", ".join(answers)  + "\n"

    survey_file.write(survey_line)
    survey_file.close()

    reconnect.updatePosition(subj_id, "dice_roll")
    push("hidden", ".survey")

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

    # Grab all of the treatment options from the subject's dictionary
    chem_treatment = reconnect.grabValue(subj_id, "chem_treatment")
    conc_treatment = reconnect.grabValue(subj_id, "conc_treatment")
    price_treatment = reconnect.grabValue(subj_id, "price_treatment")
    phys_treatment = reconnect.grabValue(subj_id, "phys_treatment")
    info_type = reconnect.grabValue(subj_id, "info_type")
    selections = reconnect.grabValue(subj_id, "selections")

    # Write everything to a file
    output_file = open(data_filepath1, "a")
    output_lines = [
      (str(subj_id) + ", " + info_type + ", " + str(choice) + ", " + ", ".join(chem_treatment) + "\n"),
      (",,," + ", ".join(conc_treatment) + "\n"),
      (",,," + ", ".join(map(str, price_treatment))  + "\n"),
      (",,," + ", ".join(phys_treatment)  + "\n"),
      (",,," + ", ".join(selections) + "\n")
    ]

    for line in output_lines:
      output_file.write(line)

    output_file.close()
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
    add("<p>Are you willing to " + phys_treatment[choice] +" containing "
      + chem_treatment[choice] + " at a concentration of " +
      conc_treatment[choice] + " parts per billion for $" + str("{0:.2f}".format(price_treatment[choice]))
      + "?</p>",
      "#selected-option")

    let(choice + 1, "#final_choice")
    let(yesorno, "#subj_final_choice")
    let(str("{0:.2f}".format(gained)), "#gained")
    let(str("{0:.2f}".format(money)), "#money")



# Generate a random price based on a mean of 10 and a standard deviation
# of 5. Using an inverse normal distribution to determine the price.
def gen_price():
  std_dev = 5.00
  h = 10.00
  i = 0.02
  j = 250.00
  k = 0.98
  x = (h - i * j) / k
  a = norm.ppf(rand.random(), x, std_dev)
  b = a
  if a < 0:
    b = 0
  if a > (2 * x):
    b = 2 * x
  d = norm.ppf(rand.random(), 250, 100)
  e = d
  if d < 0:
    e = 0
  if d > (2 * j):
    e = 2 * j

  if rand.random() < k:
	price = b
  else:
	price = e
  return price

# Generate a random integer based on a num and update the dice in the html
def dice_number(num):
  newnum = rand.randint(1, num)
  let(str(newnum), "#dice-number")
  poke("value", str(newnum), "#dice-number")
  return newnum
