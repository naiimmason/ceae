from willow.willow import *
import mod.utilities

def start(subj_id, me):
  let("")
  mod.utilities.updateStage(subj_id, "Part C instructions")

  # Show the instructions page and wait for input
  add(open("pages/subject/partc_instructions.html"))

  communication = take({"tag": "communication"})
  put(communication)
  if communication["communication"]:
    add("You will be given 5 minutes time for communication within your group before each task. This communication will be done via a chat box on your computer. This chat box allows you to send messages to everyone in the room. Please use your keyboard to type your messages and then click submit for everyone to see your message. All communication must be done through the chat box, please remain quiet. The chat box will time out after 5 minutes. Once the 5 minutes are over, no further communication is permitted.   ","#comm")
    
  take({"tag": "click", "id": "continue", "client": me})
  let("")

  mod.utilities.setPosition(subj_id, "waitingPartC")
