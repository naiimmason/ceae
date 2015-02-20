from willow.willow import *

def start(me, out_filepath):
  add(open("pages/monitor.html"))
  output_file = open(out_filepath, "w")
  output_file.write("subject number, subject id, quality, offer, accept?\n")
  output_file.close()
