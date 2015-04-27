var mongoose = require("mongoose");
var Schema = mongoose.Schema;

var userSchema = new Schema({
  number: String,
  updated: { type: Date, default: Date.now },
  farmerid: Number,
  firstname: String,
  lastname: String
});

module.exports = mongoose.model("User", userSchema);
