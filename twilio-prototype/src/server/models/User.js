var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var userSchema = new Schema({
  number: String,
  updated: { type: Date, default: Date.now },
  farmerid: Number,
  firstname: String,
  lastname: String,
  salutation: String,
  bank: { type: Number, default: 0 },
  contractType: String,
  watermeterNumber: String,
  missedPeriods: [{ type: Schema.Types.ObjectId, ref: 'ReportPeriod' }],
  submittedPeriods: [{ type:Schema.Types.ObjectId, ref: 'ReportPeriod' }]
});

module.exports = mongoose.model('User', userSchema);
