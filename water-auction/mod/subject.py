from willow.willow import *
import random as rand
import consent
import ex_part1
import ex_part2
import utilities
import practice
import subj

# The main logic that runs the subject's portion of the experiment
def start(me, subj_id, waters, rand_waters, output_path):
  let("")
  temp_waters = utilities.grabInfo(subj_id)["pers_rand_waters"]
  results = utilities.grabInfo(subj_id)["results"] # This is where all data collected will be stored

  # "start" Instruction page
  if(utilities.getPosition(subj_id) == "start"):
    subj.start.start(subj_id, me)

  # "waitingPractice" Waiting for practice page
  if(utilities.getPosition(subj_id) == "waitingPractice"):
    subj.waitingPractice.start(subj_id, me)

  # "practiceInput" Practice page
  if(utilities.getPosition(subj_id) == "practiceInput"):
    subj.practice.start(subj_id)

  # "waitingPracticeResults" Waiting for practice results page
  # "practiceResults" The practice round's results
  
  # "partBInstructions" Part B instructions page
  if(utilities.getPosition(subj_id) == "partBInstructions"):
    subj.partBInstructions.start(subj_id, me)

  # "waitingPartB" Part B waiting to start page
  if(utilities.getPosition(subj_id) == "waitingPartB"):
    subj.waitingPartB.start(subj_id)

  # "partBWater1" Part B water 1 page
  if(utilities.getPosition(subj_id) == "partBWater1"):
    utilities.increment("numStage1", me)
    utilities.decrement("numStart", me)
    results = ex_part1.start(me, subj_id, waters, temp_waters, 0)

  # "partBWater2" Part B water 2 page
  if(utilities.getPosition(subj_id) == "partBWater2"):
    results = ex_part1.start(me, subj_id, waters, temp_waters, 1)

  # "partBWater3" Part B water 3 page
  if(utilities.getPosition(subj_id) == "partBWater3"):
    results = ex_part1.start(me, subj_id, waters, temp_waters, 2)

  # "partCInstructions" Part C instructions page
  if(utilities.getPosition(subj_id) == "partCInstructions"):
    subj.partCInstructions.start(subj_id, me)

  # "waitingPartC" Waiting for part C page
  if(utilities.getPosition(subj_id) == "waitingPartC"):
    utilities.decrement("numStage1", me)
    utilities.increment("numFinishedStage1", me)
    subj.waitingPartC.start(subj_id, me)

  advance = take({"advance": True, "client": utilities.findAdmin(), "stage": 3})
  put(advance)
  median_values = advance["median"] # Grab median values from advance packet
  all_water = advance["all_water"]

  # "partCWater1" Part c water 1 page
  if(utilities.getPosition(subj_id) == "partCWater1"):
    # Update the numbers of where people are
    utilities.decrement("numFinishedStage1", me)
    utilities.increment("numStage2", me)
    results = ex_part2.start(me, subj_id, waters, rand_waters, median_values, all_water, 0, output_path)

  # "partCWater2" Part c water 2 page
  if(utilities.getPosition(subj_id) == "partCWater2"):
    results = ex_part2.start(me, subj_id, waters, rand_waters, median_values, all_water, 1, output_path)

  # "partCWater3" Part c water 3 page
  if(utilities.getPosition(subj_id) == "partCWater3"):
    results = ex_part2.start(me, subj_id, waters, rand_waters, median_values, all_water, 2, output_path)

  # "results" Results page
  if(utilities.getPosition(subj_id) == "results"):
    subj.results.start(subj_id, me, output_path, waters, median_values)

  # "endSurvey" Survey page
  if(utilities.getPosition(subj_id) == "survey"):
    subj.survey.start()
