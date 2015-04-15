var path = require("path"); 
var router = require("express").Router();

router.get("/", function(req, res) {
  res.sendFile(path.resolve("./client/html/index.html"));
});

router.get("/admin", loggedIn, isAdmin, function(req, res) {
  res.sendFile(path.resolve("./client/html/admin.html"));
});

// Check to see if a user is logged in, if not, redirect them
function loggedIn(req, res, next) {
  if (req.user) {
    next();
  } else {
    console.log("not logged in");
    res.redirect("/");
  }
}

// Check to see if they are on the admin list or not
function isAdmin(req, res, next) {
  var admin = false;

  for(var i = 0; i < admins.length; i++) {
    if (req.user.id === admins[i]) {
      admin = true;
    }
  }
  
  if (admin) {
    next();
  }
  else {
    res.redirect("/");
  }
}

module.exports = router;
