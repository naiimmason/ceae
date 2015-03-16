################################################################################
# This is the subject class that runs all code relating to the client. Here 
# the relavent HTML files will be opened their choices will be scraped and 
# calculated and the prices of the oysters will be determined.
################################################################################

# This is the main method for subjects and will be the first thing that is 
# called
def start(me, subj_id):
  let("")
  add(open("pages/subject.html"))
