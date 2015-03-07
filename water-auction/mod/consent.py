from willow.willow import *

# Wait for the person to consent and input a valid id
def waitForConsent(me):
  # Begin thread logic
  next_page = False
  consent = False
  valid_name = False
  
  # Make sure the subject has consented to the experiment and that they have 
  # filled in the ID parameter
  while consent == False or subj_id == "" or next_page == False or valid_name == False:
    next_page = False

    # Wait for the person to press continue or to press the consent button
    action = take({"tag": "click", "id": "consentSubmit", "client": me},
                  {"tag": "click", "id": "consent", "client": me},
                  {"tag": "click", "id": "reconnect", "client": me})

    # check to see which button they pressed and toggle appropriate value
    if action["id"] == "consent":
      consent = not consent
    elif action["id"] == "consentSubmit":
      next_page = True
    elif action["id"] == "reconnect":
      return "reconnect123456789"

    # Peek at their subject ID to update it
    subj_id = peek("#idInput")
    valid_name = checkUserID(subj_id);

  return subj_id


# Check to see if a subject id has already been taken or not
def checkUserID(subj_id):
  totalUsers = take({"tag": "totalSubjects"})
  put(totalUsers)
  for user in totalUsers["users"]:
    if user == subj_id:
      add("<button class=\"btn btn-lg btn-danger\" id=\"warningBtn\">The partici"
        + "pant ID is taken!</button><br><br>", "#warning")
      return False
  return True

