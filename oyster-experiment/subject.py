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
bank = 10.0
treatments = ["unknown", "low", "moderate", "high"]

# This is the main method for subjects and will be the first thing that is 
# called
def start(me, subj_id):
  rand_treatments = rand.sample(treatments, len(treatments))
  rand_treatments += rand.sample(treatments, len(treatments))
  let("")
  add(open("pages/subject.html"))

  # The initial load shows them only the instructions, wait for them to go to 
  # the bottom and click continue and then reveal the next thing.
  take({"tag": "click", "client": me, "id": "continue"})
  push("hidden", ".instructions")
  pop("hidden", ".number-selection")

  # :ets them choose the amount of oysters they want, wait for them to choose
  # and continue
  take({"tag": "click", "client": me, "id": "continue"})
  num_oysters = int(peek("#num-oysters"))
  let(str(num_oysters), "#number-of-oysters")

  # Generate 8 random prices (2 for each treatment) and add a relavent option 
  # for the user
  for i in range(8):
    # Generate the random price and calculate totals and how much the user would
    # have to subsidize
    price = gen_price()
    total_price = price * num_oysters
    you_pay = total_price - bank
    if you_pay < 0:
      you_pay = 0.00

    # Add the elements to the html
    add("<img src=\"images/noaa-graphic.png\">" +
      "<p>Oysters from <strong>" + rand_treatments[i]  + "</strong> nutrient levels:</p>" +
      "<table><thead>" +
      "<th>Price per Oyster</th>" +
      "<th>Total Cost</th>" +
      "<th>You Pay</th>" +
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
    # <form>"
    #     "<input type=\"radio\" name=\"oyster" + str(i) + "\" value=\"Yes\"> Yes" +
    #     "<input type=\"radio\" name=\"oyster" + str(i) + "\" value=\"No\"> No" +
    #     "</form>

  push("hidden", ".number-selection")
  pop("hidden", ".oyster-selection")

  # Wait for them to select and continue to the selection screen
  take({"tag": "click", "client": me, "id": "continue"})
  push("hidden", ".oyster-selection")
  pop("hidden", ".treatment-selection")

  take({"tag": "click", "client": me, "id": "submit"})
  push("hidden", ".treatment-selection")
  pop("hidden", ".thank-you")

# Generate a random oyster price based on a mean of 1.50 and a standard deviation
# of 0.50. Using an inverse normal distribution to determine the price.
def gen_price():
  price = norm.ppf(rand.random(), mean, std_dev)
  if price < 0:
    price = 0
  return price
