var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var userSchema = new Schema({
  invitationid: Number,
  number: String,
  email: String,
  payment: String,
  updated: { type: Date, default: Date.now },
  firstname: String,
  lastname: String,
  salutation: String,
  bank: { type: Number, default: 0 },
  contractType: String,
  watermeters: [{ type: Schema.Types.ObjectId, ref: 'WaterMeter' }]
});

module.exports = mongoose.model('User', userSchema);
