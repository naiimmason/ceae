var mongoose = require("mongoose");
var Schema = mongoose.Schema;

var messageSchema = new Schema({
  sender: String,
  body: String,
  date: Date,
  sid: String,
});

module.exports = mongoose.model("Message", messageSchema);
