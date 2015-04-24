################################################################################
# This is the subject class that runs all code relating to the client. Here 
# the relavent HTML files will be opened their choices will be scraped and 
# calculated and the prices of the oysters will be determined.
################################################################################
from willow.willow import *
from scipy.stats import norm
import random as rand
import reconnect

# Constant values to be used throughout the program that do not change from 
# user to user
mean = 1.50 # used for calculating the random prices
std_dev = 0.60
bank = 10.0
nutrients = ["unknown", "low", "moderate", "high"]
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


# This is the main method for subjects and will be the first thing that is 
# called
def start(me, subj_id, datafilepath1, datafilepath2, surveyfilepath1, surveyfilepath2):
  let("")
  add(open("pages/subject.html"))

  # The initial load shows them only the instructions, wait for them to go to 
  # the bottom and click continue and then reveal the next thing.
  if reconnect.getPosition(subj_id) == "start":
    pop("hidden", ".instructions")
    take({"tag": "click", "client": me, "id": "continue"})
    reconnect.updatePosition(subj_id, "number-selection")

  if reconnect.getPosition(subj_id) == "number-selection":
    push("hidden", ".instructions")
    pop("hidden", ".number-selection")

    # Lets them choose the amount of oysters they want, wait for them to choose
    # and continue
    num_oysters = -1
    while num_oysters == -1:
      take({"tag": "click", "client": me, "id": "continue"})
      num_oysters = int(peek("#num-oysters"))

      # If they do not choose a number of oysters warn them
      if num_oysters == -1:
        let("", ".warning")
        sleep(.25)
        let("<p>You must select a number of oysters.</p>", ".warning")

    reconnect.updateValue(subj_id, "num-oysters", num_oysters)
    reconnect.updatePosition(subj_id, "experiment")

  num_oysters = reconnect.grabValue(subj_id, "num-oysters")
  let("", ".warning")
  let(str(num_oysters), "#number-of-oysters")

  if reconnect.getPosition(subj_id) == "experiment":
    # Determine which experiment that the subject with choose and then store their
    # experiment choice in case that they disconnect
    experiment_choice = reconnect.grabValue(subj_id, "experiment")
    if experiment_choice == None:
      reconnect.incTreat()
      if reconnect.getTreat() % 4 != 0:
        experiment_choice = "maik"
      else:
        experiment_choice = "yosef"
      reconnect.updateValue(subj_id, "experiment", experiment_choice)

    # Route them to the correct experiment
    if experiment_choice == "maik":
      experiment1(me, subj_id, num_oysters)
    elif experiment_choice == "yosef":
      experiment2(me, subj_id, num_oysters)

    reconnect.updatePosition(subj_id, "survey")

  experiment_choice = reconnect.grabValue(subj_id, "experiment")
  num_options = 6
  if experiment_choice == "maik":
    num_options = 8

  # Show them the survey and then make sure that they have answered everything
  # that they want to by adding a warning upon the first click
  if reconnect.getPosition(subj_id) == "survey":
    push("hidden", ".oyster-selection")
    pop("hidden", ".survey")

    take({"tag": "click", "id": "submitSurvey", "client": me})
    let("<p>Please make sure you have answered all questions possible. You will NOT be able to go back.</p>", ".warning")
    take({"tag": "click", "id": "submitSurvey", "client": me})
    let("", ".warning")

    # GRAB VALUES
    values_to_grab = [
      "#age",
      "#gender",
      "#amtoysters",
      "#primshop",
      "#profession",
      "#otherprofession",
      "#political",
      "#otherpolitical",
      "#income",
      "#education",
      "#beachtime",
      "#firsttime",
      "#ofteneatseafood",
      "#ofteneatrestaurant",
      "#percentSeafoodRes",
      "#homevres",
      "#shopper",
      "#owncatch",
      "#locoyster",
      "#delawarebay",
      "#delawareinlandbay",
      "#oysterprep",
      "#oysterprepother",
      "#oysterSpec",
      "#oysterShell",
      "#oysterMeat",
      "#oysterApp",
      "#oysterSalt",
      "#oysterSmell",
      "#oysterShellColor",
      "#oysterMeatColor",
      "#oysterLoc",
      "#responders",
      "#BluesGolden",
      "#AmberSun",
      "#TillerBrown",
      "#InletIPA",
      "#OldCourt"
      # "#NightStalkStout",
      # "#DEOysterStout",
      # "#BBIPA",
      # "#RegalEagle",
      # "#KillerTiller",
      # "#CageFight",
      # "#DryHopper",
      # "#ChocRumCherr",
      # "#BabyLunchIPA",
      # "#PeteDept"
    ]

    responses = []
    for value in values_to_grab:
      responses.append(str(peek(value)))

    print responses
    reconnect.updateValue(subj_id, "survey-answers", responses)
    reconnect.updatePosition(subj_id, "consumption-selection")

  if reconnect.getPosition(subj_id) == "consumption-selection":
    push("hidden", ".survey")
    pop("hidden", ".consumption-selection")

    # Ask them which way they would like their oysters served and make sure they
    # provide an answer
    cook_option = "-1"
    while cook_option == "-1":
      take({"tag": "click", "client": me, "id": "continue"})
      cook_option = str(peek("#cooked-option"))

      # If they do not choose a consumption option, warn them
      if cook_option == "-1":
        let("", ".warning")
        sleep(.25)
        let("<p>You must select a way to receive your oysters.</p>", ".warning")

    let("", ".warning")
    reconnect.updateValue(subj_id, "cooked-option", cook_option)
    reconnect.updatePosition(subj_id, "dice-roll")

  # A random dice roll phase where subjects randomly choose a selection option
  if reconnect.getPosition(subj_id) == "dice-roll":
    push("hidden", ".consumption-selection")
    pop("hidden", ".dice-roll")

    take({"tag": "click", "client": me, "id": "dice-button"})
    poke("value", "stop", "#dice-button", )
    
    let("Stop", "#dice-button")

    stop = False
    while not stop:
      sleep(.02)
      dice_number(num_options)
      action = grab({"tag": "click", "client": me, "id": "dice-button"})
      if action != None:
        stop = True

    poke("value", "continue", "#dice-button")
    let("Continue", "#dice-button")

    take({"tag": "click", "client": me, "id": "dice-button"})
    avalue = int(peek("#final-option"))
    reconnect.updateValue(subj_id, "final-selection", avalue)


    # grab all values and write everything to the files
    filepath = ""
    surveypath = ""
    if experiment_choice == "maik":
      filepath = datafilepath1
      surveypath = surveyfilepath1
    else:
      filepath = datafilepath2
      surveypath = surveyfilepath2

    firstline = str(subj_id) + ", " + str(reconnect.grabValue(subj_id, "treatment")) \
      + ", " + str(num_oysters) + ", " + str(reconnect.grabValue(subj_id, "cooked-option")) \
      + ", " + str(reconnect.grabValue(subj_id, "final-selection"))

    options_chosen = reconnect.grabValue(subj_id, "rand_order")
    for option in options_chosen:
      firstline += ", " + str(option.replace(",", ""))
    firstline += "\n"

    secondline = ",,,,"
    values_chosen = reconnect.grabValue(subj_id, "rand_prices")
    for value in values_chosen:
      secondline += ", " + str(value)
    secondline += "\n"

    selections_chosen = reconnect.grabValue(subj_id, "selections")
    thirdline = ",,,,"
    for selection in selections_chosen:
      thirdline += ", " + str(selection)
    thirdline += "\n"

    datafile = open(filepath, "a")
    datafile.write(firstline)
    datafile.write(secondline)
    datafile.write(thirdline)
    datafile.close()

    add("<p>" + firstline + secondline + thirdline + "</p>", clients=0)

    survey_answers = reconnect.grabValue(subj_id, "survey-answers")
    linetowrite = str(subj_id)
    for answer in survey_answers:
      linetowrite += ", " + str(answer)
    linetowrite += "\n"

    surveyfile = open(surveypath, "a")
    surveyfile.write(linetowrite)
    surveyfile.close()

    add("<p>" + linetowrite + "</p>", clients=0)

    reconnect.updatePosition(subj_id, "end")

  # The ending where they are shown which option was chosen and if they decided
  # to get that option
  if reconnect.getPosition(subj_id) == "end":
    push("hidden", ".dice-roll")
    pop("hidden", ".thank-you")

    option_choice = reconnect.grabValue(subj_id, "final-selection")
    let(option_choice, "#option-choice")

    option_prices = reconnect.grabValue(subj_id, "rand_prices")
    options = reconnect.grabValue(subj_id, "rand_order")

    price = option_prices[option_choice - 1]
    total_price = price * num_oysters
    you_pay = total_price - bank
    pay_get_label = "You Pay"
    if you_pay < 0:
      you_pay = -1 * you_pay
      pay_get_label = "You Receive"

    # Depending on the experiment generate the first line that defines the type
    # of oyster the subject is being offered
    first_line = ""
    if experiment_choice == "maik":
      first_line = "<p>Oysters are from a location with <strong><u><em>" + options[option_choice-1]  + " levels</em> of nutrients</u></strong></p>"
    elif experiment_choice == "yosef":
      first_line = "<p><strong>" + options[option_choice-1] + "</strong></p>"

    # Add the elements to the html and show the html
    add( first_line +
      "<table><thead>" +
      "<th>Price per Oyster</th>" +
      "<th>Total Cost</th>" +
      "<th>"+ pay_get_label +"</th>" +
      "</thead><tbody id=\"final-selection-body\"></tbody></table" 
      , "#final-selection")

    add("<tr>" + 
        "<td>$" + str("{0:.2f}".format(price)) + "</td>" +
        "<td>$" + str("{0:.2f}".format(total_price)) + " (" + str(num_oysters) +" X $" + str("{0:.2f}".format(price)) + ")</td>" + 
        "<td>$" + str("{0:.2f}".format(you_pay)) + "</td>" +
        "</tr>", "#final-selection-body")

    yes_or_no = reconnect.grabValue(subj_id, "selections")[option_choice-1]
    cook_option = reconnect.grabValue(subj_id, "cooked-option")
    if yes_or_no == "No":
      let("You chose <strong>no</strong> to buying these oysters and you will be paid $10.", "#yesno")
    else:
      let("You chose <strong>yes</strong> to buying these oysters. They will be served \"" +
        cook_option + "\".", "#yesno")



# This is the function that runs if they are doing Maik's experiment, Maik also
# has two treatments with different wording's A and B
def experiment1(me, subj_id, num_oysters):
  num_options = 8
  # Randomly select a treatment for the subject, this only changes the wording
  # of the selection process
  treatment = reconnect.grabValue(subj_id, "treatment")
  if treatment == None:
    if reconnect.getTreat()%4 == 1:
      treatment = "B"
    elif reconnect.getTreat()%4 == 2:
      treatment = "A"
    else:
      treatment = "C"
    reconnect.updateValue(subj_id, "treatment", treatment)

  if treatment == "A":
    let(open("pages/treatmentA.html"),".treatment-instructions")
  elif treatment == "B":
    let(open("pages/treatmentB.html"),".treatment-instructions")

  # Double up on the nutrients list and randomly order them in order to make sure
  # that there is no wording or phrasing bias for the experiment
  rand_nutrients = reconnect.grabValue(subj_id, "rand_order")
  if rand_nutrients == None:
    rand_nutrients = nutrients + nutrients
    rand_nutrients = rand.sample(rand_nutrients, len(rand_nutrients))
    reconnect.updateValue(subj_id, "rand_order", rand_nutrients)

  pop("hidden", "#noaa-instructions")
  if treatment == "C":
    push("hidden", "#noaa-instructions")
  addExperimentHTML(me, subj_id, num_oysters, rand_nutrients, "maik")

# This is Yosi's experiment, they choose 6 random wordings from things
def experiment2(me, subj_id, num_oysters):
  num_options = 6

  push("hidden", "#extra-treatments")
  rand_questions = reconnect.grabValue(subj_id, "rand_order")
  if rand_questions == None:
    rand_questions = rand.sample(worded_questions, num_options)
    reconnect.updateValue(subj_id, "rand_order", rand_questions)

  addExperimentHTML(me, subj_id, num_oysters, rand_questions, "yosef")
  return "hello"

def addExperimentHTML(me, subj_id, num_oysters, options, experiment_choice):
  # Generate a number of random prices depending on how many options they are 
  # given, 8 for Maik, 6 for Yosef
  option_prices = reconnect.grabValue(subj_id, "rand_prices")
  if option_prices == None:
    option_prices = gen_rand_prices(len(options))
    reconnect.updateValue(subj_id, "rand_prices", option_prices)

  # Generate 8 random prices (2 for each nutrient level) and add a relavent option 
  # for the user
  for i in range(len(options)):
    # Generate the random price and calculate totals and how much the user would
    # have to subsidize
    price = option_prices[i]
    total_price = price * num_oysters
    you_pay = total_price - bank
    pay_get_label = "You Pay"
    if you_pay < 0:
      you_pay = -1 * you_pay
      pay_get_label = "You Receive"

    # Depending on the experiment generate the first line that defines the type
    # of oyster the subject is being offered
    first_line = ""
    if experiment_choice == "maik":
      first_line = "<p>Oysters from a body of water with <strong><u><em>" + options[i]  + " levels</em> of nutrients</u></strong></p>"
    elif experiment_choice == "yosef":
      first_line = "<p><strong>" + options[i] + "</strong></p>"

    # Add the elements to the html and show the html
    add( "<h2>Option " + str(i+1) + ":</h2>" +
      first_line +
      "<table><thead>" +
      "<th>Price per Oyster</th>" +
      "<th>Total Cost</th>" +
      "<th>"+ pay_get_label +"</th>" +
      "</thead><tbody id=\"treatment-" + str(i) + "-table\"></tbody></table" 
      , "#treatment-" + str(i))

    add("<tr>" + 
        "<td>$" + str("{0:.2f}".format(price)) + "</td>" +
        "<td>$" + str("{0:.2f}".format(total_price)) + " (" + str(num_oysters) +" X $" + str("{0:.2f}".format(price)) + ")</td>" + 
        "<td>$" + str("{0:.2f}".format(you_pay)) + "</td>" +
        "</tr>", "#treatment-" + str(i) + "-table")

    add("<p>Do you want to buy these " + str(num_oysters) + " oysters at $" + str("{0:.2f}".format(price)) 
        + " per oyster?" +
        "<div class=\"half\"><input type=\"radio\" name=\"oyster" + str(i) + "\" value=\"Yes\"> <label class=\"yesnolabel\">YES</label></div>" +
        "<div class=\"half\"><input type=\"radio\" name=\"oyster" + str(i) + "\" value=\"No\"> <label class=\"yesnolabel\">NO</label></div>" +
        "", "#treatment-" + str(i))

  push("hidden", ".number-selection")
  pop("hidden", ".oyster-selection")

  # Wait for them to select a chocie for all of them and continue to the 
  # selection screen
  selections = ["-1", "-1", "-1", "-1", "-1", "-1"]
  if experiment_choice == "maik":
    selections.append("-1")
    selections.append("-1")

  selected = False

  while not selected:
    take({"tag": "click", "client": me, "id": "continue"})

    for i in range(len(selections)):
      selections[i] = str(peek("#treatment-" + str(i) + "-sel"))

    selected = True

    for i in range(len(selections)):
      if selections[i] == "-1":
        selected = False
        let("", ".warning")
        sleep(.25)
        let("<p>You must select a choice for <strong>all</strong> options.</p>", ".warning")
        break;

  reconnect.updateValue(subj_id, "selections", selections)
  let("", ".warning")

# Generate a random oyster price based on a mean of 1.50 and a standard deviation
# of 0.50. Using an inverse normal distribution to determine the price.
def gen_price():
  price = norm.ppf(rand.random(), mean, std_dev)
  if price < 0:
    price = 0
  return price

# Generate x number of random prices and return it as an array
def gen_rand_prices(num):
  nums = []
  for i in range(num):
    nums.append(gen_price())
  return nums

def dice_number(num):
  newnum = rand.randint(1, num)
  let(str(newnum), "#dice-number")
  let(str(newnum), "#final-option")
  poke("value", str(newnum), "#dice-number")
