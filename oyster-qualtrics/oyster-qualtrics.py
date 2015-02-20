from willow.willow import *
import datetime

datetime.datetime.now().isoformat()
out_filepath = "db/data" + datetime.datetime.now().isoformat() + ".csv"

def session(me):
  # Edit document title and open up starting page, index.html
  let("Oyster Experiment", "title")

  # If you are not the monitor
  if me == 0:
    import mod.monitor
    mod.monitor.start(me, out_filepath)

  else:
    import mod.subject
    mod.subject.start(me, out_filepath)

run(session)
