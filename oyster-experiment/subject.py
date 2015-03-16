################################################################################
# This is the subject class that runs all code relating to the client. Here 
# the relavent HTML files will be opened their choices will be scraped and 
# calculated and the prices of the oysters will be determined.
################################################################################
from willow.willow import *
from scipy.stats import norm
import random as rand

mean = 1.50
std_dev = 0.50

# This is the main method for subjects and will be the first thing that is 
# called
def start(me, subj_id):
  # The inital page load lets them choose the amount of oysters they want, wait
  # for them to choose and continue
  let("")
  add(open("pages/subject.html"))
  take({"tag": "click", "client": me, "id": "continue"})
  num_oysters = int(peek("#num-oysters"))
  
  # For the amount of oysters that they chose generate a random price and add 
  # a relavent option for the user
  for i in range(num_oysters):
    price = gen_price()
    total_price = price * num_oysters
    add("<form>" + 
        str(num_oysters) + " oysters at $" +
        str("{0:.2f}".format(price)) +
        " for a total of $" + str("{0:.2f}".format(total_price)) +
        "<input type=\"radio\" name=\"oyster" + str(i) + "\" value=\"Yes\"> Yes" +
        "<input type=\"radio\" name=\"oyster" + str(i) + "\" value=\"No\"> No" +
        "</form>", ".oyster-list")

  push("hidden", ".number-selection")
  pop("hidden", ".oyster-selection")

  # Wait for them to select and continue
  take({"tag": "click", "client": me, "id": "continue"})
  push("hidden", ".oyster-selection")
  pop("hidden", ".thank-you")

# Generate a random oyster price based on a mean of 1.50 and a standard deviation
# of 0.50. Using an inverse normal distribution to determine the price.
def gen_price():
  price = norm.ppf(rand.random(), mean, std_dev)
  if price < 0:
    price = 0
  return price
