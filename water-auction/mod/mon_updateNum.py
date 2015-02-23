from willow.willow import *

def update(tag):
  answer = take({"tag": tag})
  answer["num"] += 1
  let(answer["num"], "#" + answer["tag"], clients=0)
  put(answer)
