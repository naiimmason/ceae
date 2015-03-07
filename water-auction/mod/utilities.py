from willow.willow import *

# function to convientel find out who the admin is
def findAdmin():
  admin = take({"tag": "adminUser"})
  put(admin)
  return admin["clientNum"]

# Update the number of participents started or finished and then update the 
# monitor HTML
def increment(tag, me):
  # find the dictionary coresponding to that tag and increment the num by 1 while
  # adding the user to the list of users at that point
  answer = take({"tag": tag})
  answer["num"] += 1
  answer["clients"].append(me)
  put(answer)

  # Find the admin and update the admin html
  let(answer["num"], "#" + answer["tag"], clients=findAdmin())

# Decrease the number of participents at a given point based on a tag
def decrement(tag, me):
  # Find the dictionary and decrease the number by one
  answer = take({"tag": tag})
  answer["num"] -= 1
  put(answer)

  # Find admin and update the html
  let(answer["num"], "#" + answer["tag"], clients=findAdmin())

# Update the users in the totalSubjects dictionary
def addUser(subj_id, me):
  increment("totalSubjects", me)
  totalUsers = take({"tag": "totalSubjects"})
  totalUsers["users"].append(subj_id)
  put(totalUsers)

# Create a new table row on the admin panel for the specified subject
def addUserRow(subj_id):
  # Add the table element to the correct place and add ids based on the subject
  # id
  add("<p>" + str(subj_id) + " has started the experiment</p>", "#experimentData", clients=findAdmin())
  add("<tr id=\"" + str(subj_id) + "\"><td>" + str(subj_id) + "</td>"
    "<td id=\"" + str(subj_id) + "STAGE\">Instructions</td>" # stage
    "<td id=\"" + str(subj_id) + "water1A\"></td>" # water 1 A
    "<td id=\"" + str(subj_id) + "water2A\">""</td>" # water 2 A
    "<td id=\"" + str(subj_id) + "water3A\">""</td>" # water 3 A
    "<td>""</td>" # 
    "<td id=\"" + str(subj_id) + "water1B\">""</td>" # water 1 B
    "<td id=\"" + str(subj_id) + "water2B\">""</td>" # water 2 B
    "<td id=\"" + str(subj_id) + "water3B\">""</td>" # water 3 B
    "</tr>", "#tableBody",clients=findAdmin())
