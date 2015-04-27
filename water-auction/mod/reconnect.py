from willow.willow import *

# Wait for the person to input a correct ID to reconnect with
def wait(me):
  valid_id = False
  subj_id = ""
  while not valid_id:
    action = take({"tag": "click", "client": me, "id": "reconnect"})
    subj_id = peek("#idInput")
    valid_id = checkID(subj_id)
  return subj_id
    
# Check to see if an id is valid or not
def checkID(subj_id):
  user = grab({"tag": "userInfo", "user": subj_id})
  if user is not None:
    put(user)
    return True
  else:
    add("<button class=\"btn btn-lg btn-danger\" id=\"warningBtn\">That partici"
        + "pant ID has not been used yet.</button><br><br>", "#warning")
    return False
