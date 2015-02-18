from willow.willow import *

def session(me):
  let("Oyster Experiment", "title")
  add(open("index.html")) 
  take({"tag": "click", "id": "consentSubmit"})
  stu_id = peek("#idInput")

run(session)
