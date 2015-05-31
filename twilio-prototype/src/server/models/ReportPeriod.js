var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var reportPeriodSchema = new Schema({
  startDate: Date,
  endDate: Date,
  messageids: [{ type: Schema.Types.ObjectId, ref: 'Message' }],
  submittedMeters: [{ type: Schema.Types.ObjectId, ref: 'WaterMeter' }],
  missedMeters: [{ type: Schema.Types.ObjectId, ref: 'WaterMeter' }]
});

module.exports = mongoose.model('ReportPeriod', reportPeriodSchema);
