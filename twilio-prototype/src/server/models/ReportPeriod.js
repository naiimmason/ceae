var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var reportPeriodSchema = new Schema({
  startDate: Date,
  endDate: Date,
  messageids: [{type: Schema.Types.ObjectId, ref: 'Message'}]
});

module.exports = mongoose.model('ReportPeriod', reportPeriodSchema);
