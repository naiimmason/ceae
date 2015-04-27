from willow.willow import *
from willow.branch import *
import time

def session(me):
    add(open("chat.html"))
    add(str(me),"#nameDisplay")
                                        #chatbox should run in the background to send and receive messages
    def chatbox():

        members = me + 1
                                        #you've entered the chat
        for i in range(me):
            put({"tag":"entered","client":me,"viewer":i})
        while True:
                                    #wait for a send or enter chat event
                                    #TODO respond to press 'enter' events
            msg = take({"tag":"click","id":"chatbutton","client" : me},
                       {"tag" : "chat", "receiver":me},
                       {"tag":"entered", "viewer":me},
                       {"tag":"key", "value":"\r", "client":me})
                                    #send the message to all in client list when anyone clicked on id "chatbutton"
            if msg["tag"] == "chat":
                                    #add current message
                    add(msg["msg"],"#chatbox")
                                    #someone entered the chat
            elif msg["tag"] == "entered":
                members = msg["client"] + 1
                print("total members: %s" % (members))
                                    #send a message to tell everyone that a new person entered
                txt = "Subject %s entered the chat.<br>" % (str(msg["client"]))
                add(txt,"#chatbox")
                                    #clicked the send button
            elif msg["tag"] == "click":
                                    #message cannot be empty
                if peek("#chatbar") != "":
                    label = "Subject " + str(msg["client"])
                                    #construct message
                    txt = "%s %s %s<br>" % ( time.strftime("%H:%M:%S"),
                           label,
                           peek("#chatbar",me) )
                    for i in range(members):
                        put({"tag" : "chat","sender":me,"msg":txt, "receiver": i})
                    poke("value","","#chatbar")
            elif msg["tag"] == "key":
                                                    #message cannot be empty
                if peek("#chatbar") != "":
                    label = "Subject " + str(msg["client"])
                                    #construct message
                    txt = "%s %s %s<br>" % ( time.strftime("%H:%M:%S"),
                           label,
                           peek("#chatbar",me) )
                    for i in range(members):
                        put({"tag" : "chat","sender":me,"msg":txt, "receiver": i})
                    poke("value","","#chatbar")



    background(chatbox)


run(session)
