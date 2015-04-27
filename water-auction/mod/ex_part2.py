from willow.willow import *
import random as rand
import utilities

chat_time = 300
                              #chatbox should run in the background to send and receive messages
def chatbox(me, subj_id, num):
  members = take({"tag": "chatBox" + str(num)})
  inchat = False
  for user in members["users"]:
    if user == subj_id:
      inchat = True;
      break;
  if not inchat:
    members["num"] += 1
    members["users"].append(subj_id)
  members["real_users"].append(me)
  put(members)
  users = members["real_users"]
  members = members["num"]
                                  #you've entered the chat
  for user in users:
      put({"tag":"entered","client":str(subj_id),"viewer":user})
  done = False
  seconds_left = chat_time
  while not done:
                              #wait for a send or enter chat event
                              #TODO respond to press 'enter' events
      msg = take({"tag":"click","id":"chatbutton","client" : me},
                 {"tag" : "chat", "receiver":me},
                 {"tag":"entered", "viewer":me},
                 {"tag":"key", "value":"\r", "client":me},
                 {"tag": "doneChat" + str(num)},
                 {"tag": "chatTime" + str(num), "totSeconds": seconds_left})
                              #send the message to all in client list when anyone clicked on id "chatbutton"
      if msg["tag"] == "chat":
                              #add current message
          add(msg["msg"],"#chatbox")
                              #someone entered the chat
      elif msg["tag"] == "entered":
          members += 1
          print("total members: %s" % (members))
                              #send a message to tell everyone that a new person entered
          txt = "Subject %s entered the chat.<br>" % (str(msg["client"]))
          add(txt,"#chatbox")
                              #clicked the send button
      elif msg["tag"] == "click":
                              #message cannot be empty
          if peek("#chatbar") != "":
              label = "Subject " + str(subj_id) + ":"
                              #construct message
              txt = "%s <b>%s</b> %s<br>" % ( time.strftime("%H:%M:%S"),
                     label,
                     peek("#chatbar",me).encode('utf-8').strip() )
              try:
                txt.decode('ascii')
              except UnicodeDecodeError:
                  print "it was not a ascii-encoded unicode string"
              else:
                users = take({"tag": "chatBox" + str(num)})
                put(users)
                users = users["real_users"]
                for user in users:
                    put({"tag" : "chat","sender":str(subj_id),"msg":txt, "receiver":user})
                add(txt, "#chatbox", clients=utilities.findAdmin())
              poke("value","","#chatbar")
      elif msg["tag"] == "key":
                                              #message cannot be empty
          if peek("#chatbar") != "":
              label = "Subject " + str(subj_id) + ":"
                              #construct message
              txt = "%s <b>%s</b> %s<br>" % ( time.strftime("%H:%M:%S"),
                     label,
                     peek("#chatbar",me).encode('utf-8').strip() )

              try:
                txt.decode('ascii')
              except UnicodeDecodeError:
                print "it was not a ascii-encoded unicode string"
              except UnicodeEncodeError:
                print "STILL NOT ASCII"
              else:
                print "It may have been an ascii-encoded unicode string"
                users = take({"tag": "chatBox" + str(num)})
                put(users)
                users = users["real_users"]
                for user in users:
                  put({"tag" : "chat","sender":str(subj_id),"msg":txt, "receiver":user})
                add(txt, "#chatbox", clients=utilities.findAdmin())
                poke("value","","#chatbar")
      elif msg["tag"] == "doneChat" + str(num):
        done = True
        put(msg)
      elif msg["tag"] == "chatTime" + str(num):
        # print users
        # print "SUBJECT: " + str(subj_id)
        # print "ME: " + str(me)
        seconds_left -= 1
        minutes = msg["minutes"]
        seconds = msg["seconds"]
        if seconds < 10:
          seconds = "0" + str(seconds)
        let(str(minutes) + ":" + str(seconds), "#timeLeft")
        put(msg)

# Go through each 
def start(me, subj_id, waters, temp_waters, median_values, all_water, water_pos, output_path):
  let("")
  utilities.updateStage(subj_id, "Part C water " + str(water_pos + 1))
  print all_water
  results = utilities.grabInfo(subj_id)["results"]

  # Loop through all of the water types
  i = water_pos
  add(open("pages/subject/exp_part2.html"))
  let(temp_waters[i], "#waterID")

  # Pick a random price and then wait for an answer from the client
  price = -1

  # Add results to list and log to monitor
  j = 0
  while j < len(waters):
    if temp_waters[i] == waters[j]:
      let("{0:.2f}".format(median_values[j]), "#price")
      graph_values = all_water[j];
      k = 0
      for value in graph_values:
        add("<span id=\"" + str(k) + "\" value=\"" + str(value) + "\" class=\"hidden\"></span>")
        k+=1
    j += 1
  
  add("<canvas class=\"chartFormat\" id=\"barChart" + str(i + 1) + "\" width=\"600\" height=\"250\"></canvas>", "#chartDiv4 ")


  comm = take({"tag": "communication"})
  put(comm)

  if(comm["communication"]):
    add(open("chat.html"), "#chatBox")
    add(str(subj_id),"#nameDisplay")
    chatbox(me, subj_id, water_pos)
  let("<p>Chatting has ceased!</p>", "#timer")

  add("<button type=\"button\" class=\"btn btn-lg\" id=\"Yes\">Yes</button>", "#buttonYes")
  add("<button type=\"button\" class=\"btn btn-lg\" id=\"No\">No</button>", "#buttonNo")

  answer = take({"tag": "click", "id": "Yes", "client": me},
                {"tag": "click", "id": "No", "client": me})

  # Add results to list and log to monitor
  j = 0
  while j < len(waters):
    if temp_waters[i] == waters[j]:
      results[j + 3] = answer["id"]
      add(str(answer["id"]), "#" + str(subj_id) + "water" + str(j + 1) + "B",clients=utilities.findAdmin()) 
    j += 1

  info = take({"tag": "userInfo", "user": subj_id})
  info["results"] = results
  put(info)

  if(i == 0):
    comm = take({"tag": "communication"})
    put(comm)

    if(comm["communication"]):
      utilities.setPosition(subj_id, "partCWater2Wait")
    else:
      utilities.setPosition(subj_id, "partCWater2")
  elif(i == 1):
    comm = take({"tag": "communication"})
    put(comm)

    if(comm["communication"]):
      utilities.setPosition(subj_id, "partCWater3Wait")
    else:
      utilities.setPosition(subj_id, "partCWater3")
  elif(i == 2):
    utilities.setPosition(subj_id, "results")
    results = utilities.grabInfo(subj_id)["results"]

    # Make clientData dictionary and push on to Stack
    clientData2 = { "client": me, "tag": "clientData2", "results": results, "user": subj_id }
    put(clientData2)
    # Log data
    add("<p><b>" + subj_id + "</b> finished: " + ", ".join(clientData2["results"]) + "</p>", "#experimentData", clients=utilities.findAdmin())

    # Update numbers of where people are
    utilities.decrement("numStage2", me)
    utilities.increment("numFinished", me)
    prac_results = utilities.grabInfo(subj_id)["practice_results"]


    # Output the answer and data to the relavent database file
    output_file = open(output_path, "a")
    output_file.write(str(me) + ", " + str(subj_id) + ", " + str(prac_results[0]) + ", "  + str(prac_results[1]) + ", " + str(results[0]) + ", " + str(results[1]) + ", " + str(results[2]) + ", " + str(results[3]) + ", " + str(results[4]) + ", " + str(results[5]) +  "\n")
    output_file.close()

  return results

def wait(me, subj_id, water):
  let("")
  utilities.updateStage(subj_id, "Waiting for Part C Water " + str(water))
  add(open("pages/subject/waiting_partc.html"))
  advance = take({"advance": True, "stage": "waitingPartC" + str(water)})
  put(advance)
  utilities.setPosition(subj_id, "partCWater" + str(water))
