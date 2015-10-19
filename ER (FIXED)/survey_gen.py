input_filepath = "questions.txt"
output_filepath = "q_html.html"

input_file = open(input_filepath, "r")
output_file = open(output_filepath, "w")

q_num = 0
range_q_num = 0
range_qs = []
yesno_qs = []
multiple_qs = []

for line in input_file:
  html = ""
  args = line.rstrip("\n").split("\t")
  q = args[0]
  qtype = args[1]

  if qtype == "range":
    range_vals = args[2].split(",")
    min_val = str(range_vals[0])
    max_val = str(range_vals[1])
    step = str(range_vals[2]) 
    start_val = str(range_vals[3])
    first_label = str(args[3])
    last_label = str(args[4])

    html = "<li>\n  " \
      + q + " <strong><output for=\"r" + str(q_num) + "\" id=\"surveyq" + str(q_num) + "-sel\">" \
      + start_val + "</output></strong>" + \
      "\n  <div class=\"slider\">\n    " + \
      "<span>" + first_label + " (" + min_val + ")</span>" + \
      "<input id=\"r" + str(q_num) + "\" type=\"range\" value=\"" + start_val + "\" min=" + \
      "\"" + min_val + "\" max=\"" + max_val + "\" step=\"" + step + "\" oninput" + \
      "=\"outputUpdate(value, " + str(range_q_num) + ")\">" + \
      "<span>" + last_label + " (" + max_val + ")</span>" + \
      "\n  </div>\n" + "</li>\n"

    range_q_num += 1
    range_qs.append(q_num)

  if qtype == "input":
    html = "<li>\n  " \
      + q + "\n  " + \
      "<input type=\"text\" id=\"q" + str(q_num) + "\">" \
      + "\n</li>\n"

  if qtype == "yesno":
    html = "<li>\n  " \
      + "<p>" + q + "</p>\n  " \
      + "<div class=\"center\">\n    " \
      + "<div class=\"radio-item half\">\n      " \
      + "<input type=\"radio\" name=\"q" + str(q_num) + "\" value=\"Yes\">\n      " \
      + "<label>Yes</label>\n    " \
      + "</div>\n    " \
      + "<div class=\"radio-item half\">\n      " \
      + "<input type=\"radio\" name=\"q" + str(q_num) + "\" value=\"No\">\n      " \
      + "<label>No</label>\n    " \
      + "</div>\n  " \
      + "</div>\n" \
      + "</li>\n"

    yesno_qs.append(q_num)

  if qtype == "multiple":
    options = args[2].split(",")
    html = "<li>\n  " \
      + q + "\n"

    for option in options:
      html += "  <div class=\"radio-item\">\n    " \
        + "<input type=\"radio\" name=\"q" + str(q_num) + "\" value=\"" + option + "\">\n    " \
        + "<label>" + option + "</label>\n  " \
        + "</div>\n"

    html += "</li>\n"
    multiple_qs.append(q_num)


  q_num += 1
  output_file.write(html)

string_rangeqs = []
for rangeq in range_qs:
  string_rangeqs.append("#surveyq" + str(rangeq) + "-sel")

html = ""
string_yesnoqs = []
for yesnoq in yesno_qs:
  string_yesnoqs.append("q" + str(yesnoq))
  html += "<textarea class=\"hidden\" id=\"surveyq" + str(yesnoq) + "-sel\"></textarea>\n"

string_multipleqs = []
for multipleq in multiple_qs:
  string_multipleqs.append("q" + str(multipleq))
  html += "<textarea class=\"hidden\" id=\"surveyq" + str(multipleq) + "-sel\"></textarea>\n"
output_file.write(html)

print range_qs
print yesno_qs
print multiple_qs

print "yesno_tags = ", string_yesnoqs
print "multiple_tags = ", string_multipleqs
print "output_update_tags = ", string_rangeqs
print "Num questions = ", q_num