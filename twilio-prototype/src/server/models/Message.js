var mongoose = require("mongoose");
var Schema = mongoose.Schema;

var messageSchema = new Schema({
  sender: String,
  body: String,
  date: { type: Date, default: Date.now },
  sid: String,
  farmerid: Number
});

module.exports = mongoose.model("Message", messageSchema);
