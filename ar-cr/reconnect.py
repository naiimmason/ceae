################################################################################
# This class is used for reconnection purposes if a subject disconnects from the
# experiment. This is a "module" and can be imported into any further experiments
# if need be. You must include this class when you add a user and if you want 
# someobdy to recoonnect at a specific spot. 
################################################################################
from willow.willow import *

# Add a user on to the stack
def addUser(subj_id):
  put({"tag": "userInfo", 
       "user": subj_id, 
       "position": "start",
       "chem_treatment": None,
       "price_treatment": None,
       "conc_treatment": None,
       "phys_treatment": None,
       "selections": None});

# Check to see if a user already exists or not
def userExist(subj_id):
  userInfo = grab({"tag": "userInfo",
                   "user": subj_id})
  if userInfo == None:
    return False
  else:
    put(userInfo)
    return True

# Update the position the subject is at
def updatePosition(subj_id, position):
  updateValue(subj_id, "position", position)

# Return what stage the user is at
def getPosition(subj_id):
  return grabValue(subj_id, "position")

# Update a value of the users
def updateValue(subj_id, valueTag, newValue):
  userInfo = grab({"tag": "userInfo",
                   "user": subj_id})
  userInfo[valueTag] = newValue
  put(userInfo)

# Grab a value from the user model
def grabValue(subj_id, valueTag):
  userInfo = grab({"tag": "userInfo",
                   "user": subj_id})
  put(userInfo)
  if userInfo[valueTag] == None:
    return None
  return userInfo[valueTag]
