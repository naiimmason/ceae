from willow.willow import *
import reconnect
import random as rand

def start(me, subj_id, data_filepath1, survey_filepath1):
  reconnect.addNumSubj();
  let("")
  add(open("pages/subject.html"))

  if reconnect.getPosition(subj_id) == "start":
    pop("hidden", ".instructions")

    # Put a message into the chat showing that a new person has entered
    newmsg = "Subject " + str(subj_id) + " has enetered the chat."
    msgdict = {"tag": "message", "content": newmsg}
    users = grab({"tag": "totalUsers"})
    put(users)
    for i in range(users["numsubjs"]):
      msgdict["me" + str(i)] = False
    put(msgdict)

    while True:
      # Check for new message or if the user has hit enter or send
      msg = take({"tag": "message", "me" + str(me): False},
                 {"tag": "click", "id": "sendbutton", "client": me},
                 {"tag": "key", "value":"\r", "client":me},)

      # A slight hack that way the elif clause works cause the key doesn't have
      # an id otherwise and the if statement breaks
      if msg["tag"] == "key":
        msg["id"] = "-1"

      # If a new message turn that you have received to true and put back for
      # everyone else and then display the message in the chatbox div element
      if msg["tag"] == "message":
        msg["me" + str(me)] = True
        put(msg)
        add(msg["content"], "#chatbox")

      # When a person sends a message create a message dictionary, cycle through
      # all users and set their received state to false so that they pick up
      # the message. Add some styling to the person's name for clarity in chat
      elif msg["id"] == "sendbutton" or msg["tag"] == "key":
        msgdict = {"tag": "message"}
        users = grab({"tag": "totalUsers"})
        put(users)
        for i in range(users["numsubjs"]):
          msgdict["me" + str(i)] = False

        newmsg = "<p style=\"margin-top:0px; margin-bottom:0px;\"><strong>" + \
          str(subj_id) + "</strong> says: "
        newmsg += peek("#chatinput")
        newmsg += "</p>"
        msgdict["content"] = newmsg
        put(msgdict)
        poke("value","","#chatinput")


  return "hello"
