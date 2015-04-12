var path = require("path"); 
var router = require("express").Router();

app.get("/", function(req, res) {
  res.sendFile(path.resolve("./client/html/index.html"));
});

module.exports = router;
