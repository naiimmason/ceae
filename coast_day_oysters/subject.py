##########################################################################
# This is the subject class that runs all code relating to the client. Here
# the relavent HTML files will be opened their choices will be scraped and
# calculated and the prices of the oysters will be determined.
##########################################################################
from willow.willow import *
from scipy.stats import norm
import random as rand
import reconnect
import datetime

# Constant values to be used throughout the program that do not change from
# user to user
mean = 1.50  # used for calculating the random prices
std_dev = 0.50
bank = 10.0
nutrients = ["unknown", "low", "moderate", "high"]
question_1 = ["Consider these oysters."];
questions_2_3 = ["Consider these oysters from the east coast.",
                 "Consider these oysters from the west coast."]
questions_4_5 = ["Consider these local oysters. Local means that these oysters" + \
                 " are grown within 25 miles of the location you are at right now.",
                 "Consider these non-local oysters. Non-local means that these oysters " + \
                 "are not grown within 25 miles of the location you are at right now."]
question_6_7_8_A = ["Consider these oysters from low nutrient waters.",
                  "Consider these oysters from moderate nutrient levels.",
                  "Consider these oysters from high nutrient levels."]
question_6_7_8_B = ["Consider these oysters from low nutrient waters <img class=\"nutrient\" src=\"images/low.png\">.",
                "Consider these oysters from moderate nutrient waters <img class=\"nutrient\" src=\"images/medium.png\">.",
                "Consider these oysters from high nutrient waters <img class=\"nutrient\" src=\"images/high.png\"."]

question_6_7_8_C = ["Consider these oysters from low nutrient waters.",
                "Consider these oysters <img class=\"droplet\" src=\"images/water_droplet.png\"> from moderate nutrient waters .",
                "Consider these oysters <img class=\"droplet\" src=\"images/water_droplet.png\"> from high nutrient waters."]

question_6_7_8_D = ["Consider these oysters from low nutrient waters.",
                "Consider these oysters <img class=\"droplet\" src=\"images/silver_droplet.png\"> from moderate      nutrient waters .",
                "Consider these oysters <img class=\"droplet\" src=\"images/gold_droplet.png\"> from high nutrient waters."]




# This is the main method for subjects and will be the first thing that is
# called
def start(me, subj_id, datafilepath, data1_path, survey1_path):
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
            experiment_choice = "maik"
            reconnect.updateValue(subj_id, "experiment", experiment_choice)

        # Run the experiment code
        experiment1(me, subj_id, num_oysters)


        # grab all values and write everything to the files
        filepath = data1_path
        datafile = open(filepath, "a")

        # grab the time and the first part of the line
        time = datetime.datetime.now().isoformat()
        firstpart = time + ", " + str(subj_id) + ", " + str(reconnect.grabValue(subj_id, "treatment")) \
            + ", " + str(num_oysters) \
            + ", "

        middle_part = ""

        options_chosen = reconnect.grabValue(subj_id, "rand_order")
        values_chosen = reconnect.grabValue(subj_id, "rand_prices")
        selections_chosen = reconnect.grabValue(subj_id, "selections")
        for i in range(len(options_chosen)):
            middle_part += str(i + 1) + ", "
            middle_part += str(options_chosen[i].replace(",", "")) + ", "
            middle_part += str(values_chosen[i]) + ", "
            middle_part += str(selections_chosen[i]) + "\n"
            datafile.write(firstpart + middle_part)
            middle_part = ""

        datafile.close()
        reconnect.updatePosition(subj_id, "logo_part")

    experiment_choice = reconnect.grabValue(subj_id, "experiment")
    num_options = 8

    if reconnect.getPosition(subj_id) == "logo_part":
        push("hidden", ".oyster-selection")
        pop("hidden", ".extra-question")
        take({"tag": "click", "id": "submit_logo", "client": me})

        reconnect.updatePosition(subj_id, "survey")

    # Show them the survey and then make sure that they have answered everything
    # that they want to by adding a warning upon the first click
    if reconnect.getPosition(subj_id) == "survey":
        push("hidden", ".extra-question")
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
            # "#responders",
            # "#BluesGolden",
            # "#AmberSun",
            # "#TillerBrown",
            # "#InletIPA",
            # "#OldCourt"
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

        # grab all values and write everything to the files
        filepath = survey1_path
        datafile = open(filepath, "a")

        # grab the time and the first part of the line
        time = datetime.datetime.now().isoformat()
        firstpart = time + ", " + str(subj_id) + ", "

        # grab the survey answers then sandwich options inbetwen these parts
        survey_answers = reconnect.grabValue(subj_id, "survey-answers")
        linetowrite = ""
        for answer in survey_answers:
            linetowrite += str(answer) + ", "
        linetowrite += "\n"

        datafile.write(firstpart + linetowrite)
        datafile.close()
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

    # A random dice roll phase where subjects randomly choose a selection
    # option
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
        filepath = datafilepath
        datafile = open(filepath, "a")

        # grab the time and the first part of the line
        time = datetime.datetime.now().isoformat()
        firstpart = time + ", " + str(subj_id) + ", " + str(reconnect.grabValue(subj_id, "treatment")) \
            + ", " + str(reconnect.grabValue(subj_id, "final-selection")) + ", " + str(num_oysters) \
            + ", " + str(reconnect.grabValue(subj_id, "cooked-option")) \
            + ", "

        # grab the survey answers then sandwich options inbetwen these parts
        survey_answers = reconnect.grabValue(subj_id, "survey-answers")
        linetowrite = ""
        for answer in survey_answers:
            linetowrite += str(answer) + ", "
        linetowrite += "\n"

        middle_part = ""

        options_chosen = reconnect.grabValue(subj_id, "rand_order")
        values_chosen = reconnect.grabValue(subj_id, "rand_prices")
        selections_chosen = reconnect.grabValue(subj_id, "selections")
        for i in range(len(options_chosen)):
            middle_part += str(i + 1) + ", "
            middle_part += str(options_chosen[i].replace(",", "")) + ", "
            middle_part += str(values_chosen[i]) + ", "
            middle_part += str(selections_chosen[i]) + ", "
            datafile.write(firstpart + middle_part + linetowrite)
            middle_part = ""

        datafile.close()

        #add_answer_to_admin(firstline, secondline, thirdline, subj_id)
        #add("<p>" + firstpart + secondline + thirdline + "</p>", clients=0)
        #
        # survey_answers = reconnect.grabValue(subj_id, "survey-answers")
        # linetowrite = str(subj_id)
        # for answer in survey_answers:
        #     linetowrite += ", " + str(answer)
        # linetowrite += "\n"
        #
        # surveyfile = open(surveypath, "a")
        # surveyfile.write(linetowrite)
        # surveyfile.close()

        #add("<p>" + linetowrite + "</p>", clients=0)

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
            first_line = "<p>" + \
                options[option_choice - 1] + \
                "</p>"
        elif experiment_choice == "yosef":
            first_line = "<p><strong>" + \
                options[option_choice - 1] + "</strong></p>"

        # Add the elements to the html and show the html
        add(first_line +
            "<table><thead>" +
            "<th>Price per Oyster</th>" +
            "<th>Total Cost</th>" +
            "<th>" + pay_get_label + "</th>" +
            "</thead><tbody id=\"final-selection-body\"></tbody></table", "#final-selection")

        add("<tr>" +
            "<td>$" + str("{0:.2f}".format(price)) + "</td>" +
            "<td>$" + str("{0:.2f}".format(total_price)) + " (" + str(num_oysters) + " X $" + str("{0:.2f}".format(price)) + ")</td>" +
            "<td>$" + str("{0:.2f}".format(you_pay)) + "</td>" +
            "</tr>", "#final-selection-body")

        yes_or_no = reconnect.grabValue(subj_id, "selections")[
            option_choice - 1]
        cook_option = reconnect.grabValue(subj_id, "cooked-option")
        if yes_or_no == "No":
            let("You chose <strong>no</strong> to buying these oysters and you will be paid $10.", "#yesno")
        else:
            let("You chose <strong>yes</strong> to buying these oysters. They will be served \"" +
                cook_option + "\".", "#yesno")


# This function runs the actual experiment, there are 4 treatments.
# A = noaa + leed
# B = leed
# C = noaa
# d = no info
def experiment1(me, subj_id, num_oysters):
    num_options = 8
    # Randomly select a treatment for the subject, this only changes the wording
    # of the selection process
    treatment = reconnect.grabValue(subj_id, "treatment")
    if treatment == None:
        if reconnect.getTreat() % 4 == 1:
            treatment = "A"
        elif reconnect.getTreat() % 4 == 2:
            treatment = "B"
        elif reconnect.getTreat() % 4 == 3:
            treatment = "C"
        else:
            treatment = "D"
        reconnect.updateValue(subj_id, "treatment", treatment)

    if treatment == "A":
        let(open("pages/treatmentA.html"), ".treatment-instructions")
    elif treatment == "B":
        let(open("pages/treatmentB.html"), ".treatment-instructions")
    elif treatment == "C":
        let(open("pages/treatmentC.html"), ".treatment-instructions")
    else:
        let(open("pages/treatmentD.html"), ".treatment-instructions")

    # Double up on the nutrients list and randomly order them in order to make sure
    # that there is no wording or phrasing bias for the experiment
    rand_options = reconnect.grabValue(subj_id, "rand_order")
    if rand_options == None:
        rand_options = [];
        rand_options.append(question_1[0])
        rand_options = rand_options + rand.sample(questions_2_3, len(questions_2_3)) + \
            rand.sample(questions_4_5, len(questions_4_5))
        if treatment == "A":
            rand_options = rand_options + rand.sample(question_6_7_8_A, len(question_6_7_8_A))
        elif treatment == "B":
            rand_options = rand_options + rand.sample(question_6_7_8_B, len(question_6_7_8_B))
        elif treatment == "C":
            rand_options = rand_options + rand.sample(question_6_7_8_C, len(question_6_7_8_C))
        else:
            rand_options = rand_options + rand.sample(question_6_7_8_D, len(question_6_7_8_D))
        reconnect.updateValue(subj_id, "rand_order", rand_options)

    addExperimentHTML(me, subj_id, num_oysters, rand_options, "maik")


def addExperimentHTML(me, subj_id, num_oysters, options, experiment_choice):
    # Generate a number of random prices depending on how many options they are
    # given, 8 for Maik, 6 for Yosef
    option_prices = reconnect.grabValue(subj_id, "rand_prices")
    if option_prices == None:
        option_prices = gen_rand_prices(len(options))
        reconnect.updateValue(subj_id, "rand_prices", option_prices)

    # Match prices with options and display questions
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
        first_line = "<p>" + options[i] + "</p>"

        # Add the elements to the html and show the html
        add("<h2>Option " + str(i + 1) + ":</h2>" +
            first_line +
            "<table><thead>" +
            "<th>Price per Oyster</th>" +
            "<th>Total Cost</th>" +
            "<th>" + pay_get_label + "</th>" +
            "</thead><tbody id=\"treatment-" + str(i) + "-table\"></tbody></table", "#treatment-" + str(i))

        add("<tr>" +
            "<td>$" + str("{0:.2f}".format(price)) + "</td>" +
            "<td>$" + str("{0:.2f}".format(total_price)) + " (" + str(num_oysters) + " X $" + str("{0:.2f}".format(price)) + ")</td>" +
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
                break

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

# def add_answer_to_admin(firstline, secondline, thridline, subj_id):
#   add("<div id=\"" + str(subj_id) + "\"></div>", "#ans-row", clients=0)
#   add("", "#" + str(subj_id), clients=0)
#   pass
