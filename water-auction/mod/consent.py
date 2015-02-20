from willow.willow import *

def waitForConsent(me):
  # Begin thread logic
  next_page = False
  consent = False
  
  # Make sure the subject has consented to the experiment and that they have filled in the ID parameter
  while consent == False or subj_id == "" or next_page == False:
    next_page = False

    # Wait for the person to press continue or to press the consent button
    action = take({"tag": "click", "id": "consentSubmit", "client": me},
                  {"tag": "click", "id": "consent", "client": me})

    # check to see which button they pressed and toggle appropriate value
    if action["id"] == "consent":
      consent = not consent
    elif action["id"] == "consentSubmit":
      next_page = True

    # Peek at their subject ID to update it
    subj_id = peek("#idInput")

  return subj_id
