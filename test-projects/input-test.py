from willow.willow import *

def session(me):
  let("Testing Input", "title")
  add(open("input-test.html"))
  add("<button type=\"button\" id=\"test-btn\" class=\"btn btn-success center-block\">Click Me</button>")
  take({"tag": "click", "id": "test-btn", "client": me})
  add("<p class=\"center\">I've been clicked!</p>", "#main-content")

run(session)
