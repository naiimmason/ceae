from willow.willow import *
import mod.monitor
import mod.subject
import random as rand

waters = ["spring water", "re-use tap water", "re-use tap water that has gone through a ZeroWater filter"]
rand_waters = rand.sample(waters, len(waters))

def session(me):
  # Edit page title
  let("Second-Price Auction", "title")

  # Check to see if proctor or not
  if me == 0:
    mod.monitor.start(me)
  else:
    mod.subject.start(me, waters, rand_waters)

run(session)
