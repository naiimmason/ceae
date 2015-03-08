from willow.willow import *
#from willow.branch import *
import time

def session(me):
    add(open("chat.html"))
    add(str(me),"#nameDisplay")
                                        #chatbox should run in the background to send and receive messages
    def chatbox():

        clientslist = []
                                        #you've entered the chat
        put({"tag":"entered","client":me})
        while True:
                                        #the server
            if me == 0:
                                        #wait for a send or enter event
                                        #TODO respond to press 'enter' events
                msg = take({"tag":"click","id":"chatbutton","client" : me},
                           {"tag" : "chat"},
                           {"tag":"entered"})
                                        #send the message to all in client list when anyone clicked on id "chatbutton"
                if msg["tag"] == "chat":
                                        #send the message to everyone in client list
                        for i in clientslist:
                            add(msg["msg"],"#chatbox", i)
                                        #TODO clear the chatbar
                                        #someone entered the chat
                elif msg["tag"] == "entered":
                    clientslist.append(msg["client"])
                                        #send a message to tell everyone that a new person entered
                    txt = "Subject %s entered the chat.<br>" % (str(msg["client"]))
                    for i in clientslist:
                        add(txt,"#chatbox", i)
                elif msg["tag"] == "click":
                                        #message cannot be empty
                    if peek("#chatbar") != "":
                        label = "Subject " + str(msg["client"])
                                        #construct message
                        txt = "%s %s %s<br>" % ( time.strftime("%H:%M:%S"),
                               label,
                               peek("#chatbar",me) )
                        put({"tag" : "chat","client":me,"msg":txt})

                                        #the clients
            else:
                msg = take({"tag":"click","id":"chatbutton","client" :me})
                                        #message cannot be empty
                if peek("#chatbar") != "":
                    label = "Subject " + str(msg["client"])
                                        #construct message
                    txt = "%s %s %s<br>" % ( time.strftime("%H:%M:%S"),
                           label,
                           peek("#chatbar",me) )
                    put({"tag" : "chat","client":me,"msg":txt})


    background(chatbox)


run(session)
