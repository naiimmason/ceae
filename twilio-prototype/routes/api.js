var router = require("express").Router()
var twilio = require("twilio");
var auth = require("../config/auth")
var twilioclient = new twilio.RestClient(auth.sid, auth.token);

router.post("/message", function(req, res) {
  //console.log(req.body);
  // client.messages.list(function(err, data) {
  //   data.messages.forEach(function(message) {
  //     console.log(message.body);
  //   });
  // });
  twilioclient.sendMessage({
    to: req.body.From,
    from: auth.number,
    body: req.body.Body
  }, function(err, text) {
    if(!err) {
      console.log("To: " + req.body.From);
      console.log('You sent: '+ text.body);
    } else {
      console.log(err);
    }
})});

module.exports = router;
