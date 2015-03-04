from willow.willow import *
import mod.monitor
import mod.subject
import random as rand
import datetime

datetime.datetime.now().isoformat()

waters = ["Penta Ultra Purified water", "re-use tap water", "re-use tap water that has gone through a ZeroWater filter"]
rand_waters = rand.sample(waters, len(waters))
output_file = "db/data" + datetime.datetime.now().isoformat() + ".csv"

def session(me):
  # Edit page title
  let("Second-Price Auction", "title")

  # Check to see if proctor or not
  if me == 0:
    mod.monitor.start(me, waters, output_file)
  else:
    mod.subject.start(me, waters, rand_waters, output_file)

run(session)
