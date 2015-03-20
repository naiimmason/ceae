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
std_dev = 0.50
bank = 10.0
nutrients = ["unknown", "low", "moderate", "high"]

# This is the main method for subjects and will be the first thing that is 
# called
def start(me, subj_id):
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

  # Determine which experiment that the subject with choose and then store their
  # experiment choice in case that they disconnect
  experiment_choice = reconnect.grabValue(subj_id, "experiment")
  if experiment_choice == None:
    if rand.random() < 2:
      experiment_choice = "maik"
    else:
      experiment_choice = "yosef"
    reconnect.updateValue(subj_id, "experiment", experiment_choice)

  # Route them to the correct experiment
  if experiment_choice == "maik":
    experiment1(me, subj_id, num_oysters)
  elif experiment_choice == "yosef":
    experiment2(me, subj_id, num_oysters)

# This is the function that runs if they are doing Maik's experiment, Maik also
# has two treatments with different wording's A and B
def experiment1(me, subj_id, num_oysters):
  # Randomly select a treatment for the subject, this only changes the wording
  # of the selection process
  treatment = "A"
  if rand.random() < .5:
    treatment = "B"

  if treatment == "A":
    let(open("pages/treatmentA.html"),".treatment-instructions")
  elif treatment == "B":
    let(open("pages/treatmentB.html"),".treatment-instructions")

  # Double up on the nutrients list and randomly order them in order to make sure
  # that there is no wording or phrasing bias for the experiment
  rand_nutrients = nutrients + nutrients
  rand_nutrients = rand.sample(rand_nutrients, len(rand_nutrients))

  # Generate 8 random prices (2 for each nutrient level) and add a relavent option 
  # for the user
  for i in range(8):
    # Generate the random price and calculate totals and how much the user would
    # have to subsidize
    price = gen_price()
    total_price = price * num_oysters
    you_pay = total_price - bank
    pay_get_label = "You Pay"
    if you_pay < 0:
      you_pay = -1 * you_pay
      pay_get_label = "You Get"

    # Add the elements to the html
    add("<p>Oysters are from a location with <strong><u><em>" + rand_nutrients[i]  + " levels</em> of nutrients</u></strong></p>" +
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

    add("<p>Would you buy these oysters at $" + str("{0:.2f}".format(price)) 
        + " per oyster?" +
        "<div class=\"half\"><input type=\"radio\" name=\"oyster" + str(i) + "\" value=\"Yes\"> Yes</div>" +
        "<div class=\"half\"><input type=\"radio\" name=\"oyster" + str(i) + "\" value=\"No\"> No</div>" +
        "", "#treatment-" + str(i))

  push("hidden", ".number-selection")
  pop("hidden", ".oyster-selection")

  # Wait for them to select a chocie for all of them and continue to the 
  # selection screen
  selections = ["-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1"]
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

  let("", ".warning")
  push("hidden", ".oyster-selection")
  pop("hidden", ".option-selection")

  take({"tag": "click", "client": me, "id": "submit"})
  push("hidden", ".option-selection")
  pop("hidden", ".thank-you")
  return "hello"

# This is Yosi's experiment, they choose 6 random wordings from things
def experiment2(me, subj_id, num_oysters):
  return "hello"

# This function is called after each of the experiment options are finished
def finishExperiment(me, subj_id):
  return "hello"

# Generate a random oyster price based on a mean of 1.50 and a standard deviation
# of 0.50. Using an inverse normal distribution to determine the price.
def gen_price():
  price = norm.ppf(rand.random(), mean, std_dev)
  if price < 0:
    price = 0
  return price
