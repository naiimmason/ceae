var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var reportPeriodSchema = new Schema({
  startDate: Date,
  endDate: Date,
  messageids: [{ type: Schema.Types.ObjectId, ref: 'Message' }],
  submittedUsers: [{ type: Schema.Types.ObjectId, ref: 'User' }],
  missedUsers: [{ type: Schema.Types.ObjectId, ref: 'User' }]
});

module.exports = mongoose.model('ReportPeriod', reportPeriodSchema);
