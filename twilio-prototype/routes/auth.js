var router = require("express").Router();
var GoogleAuth = require("../config/auth").GoogleAuth;

router.get("/google", passport.authenticate("google", { scope: "https://www.googleapis.com/auth/plus.login email" }),
           function(req, res) {});

router.get("/google/callback",
           passport.authenticate("google", { failureRedirect: "/fff" }),
           function(req, res) {
            res.redirect("/admin");
           });

router.get("/logout", function(req, res) {
  req.logout();
  res.redirect("/#/");
});

module.exports = router;
