from willow.willow import *

# Update the number of participents started or finished and then update the monitor HTML
def update(tag, me):
  answer = take({"tag": tag})
  answer["num"] += 1
  answer["clients"].append(me)
  let(answer["num"], "#" + answer["tag"], clients=0)
  put(answer)
