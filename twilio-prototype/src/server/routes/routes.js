var path = require("path");
var router = require("express").Router();

// Send the basic landing page for farmers to report their water meter usage
router.get("/", function(req, res) {
  res.sendFile(path.resolve("./src/client/html/index.html"));
});

// The admin page
router.get("/admin", loggedIn, isAdmin, function(req, res) {
  res.sendFile(path.resolve("./src/client/html/admin.html"));
});

// Check to see if a user is logged in, if not, redirect them
function loggedIn(req, res, next) {
  if (req.user) {
    next();
  } else {
    console.log("not logged in");
    res.redirect("/auth/google");
  }
}

// Check to see if they are on the admin list or not
function isAdmin(req, res, next) {
  var admin = false;

  for(var i = 0; i < admins.length; i++) {
    if (req.user.emails[0].value === admins[i]) {
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
