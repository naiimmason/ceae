from willow.willow import *
from scipy.stats import norm
import reconnect
import random as rand

# Treatments and everything defined at the top for easy access
mean = 8
std_dev = 1.50
num_questions = 6

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
      add("<p>Are you willing to " + phys_treatment[i] +" contianing " 
          + chem_treatment[i] + " at a concentration of " + 
          conc_treatment[i] + " ppb for $" + str("{0:.2f}".format(price_treatment[i])) 
          + "?</p>" +
          "<div class=\"center\"><div class=\"half\"><input type=\"radio\" name=\"question" + str(i) 
          + "\" value=\"Yes\"> <label class=\"yesnolabel\">YES</label></div>" +
          "<div class=\"half\"><input type=\"radio\" name=\"question" + str(i) 
          + "\" value=\"No\"> <label class=\"yesnolabel\">No</label></div></div>",
          ".experimentqs")
      add("<hr>", ".experimentqs")


    take({"id": "click", "tag": "submit", "client": me})

# Generate a random oyster price based on a mean of 1.50 and a standard deviation
# of 0.50. Using an inverse normal distribution to determine the price.
def gen_price():
  price = norm.ppf(rand.random(), mean, std_dev)
  if price < 0:
    price = 0
  return price