from willow.willow import *
import mod.monitor
import mod.subject

def session(me):
  # Edit page title
  let("Water Prices", "title")

  # Check to see if proctor or not
  if me == 0:
    mod.monitor.start(me)
  else:
    mod.subject.start(me)

run(session)
