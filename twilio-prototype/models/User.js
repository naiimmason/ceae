var mongoose = require("mongoose");
var Schema = mongoose.Schema;

var userSchema = new Schema({
  number: String,
  updated: { type: Date, default: Date.now }
});

module.exports = mongoose.model("User", userSchema);
