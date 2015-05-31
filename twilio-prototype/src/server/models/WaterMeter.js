var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var waterMeterSchema = new Schema({
  updated: { type: Date, default: Date.now },
  serialnumber: String,
  meterUnits: String,
  acresIrrigated: String,
  crops: String,
  missedPeriods: [{ type: Schema.Types.ObjectId, ref: 'ReportPeriod' }],
  submittedPeriods: [{ type: Schema.Types.ObjectId, ref: 'ReportPeriod' }],
  submittedValues: [{ period: { type: Schema.Types.ObjectId, ref: 'ReportPeriod'},
                      value: String,
                      date: { type: Date, default: Date.now }}],
  user: { type: Schema.Types.ObjectId, ref: 'User' }
});

module.exports = mongoose.model('WaterMeter', waterMeterSchema);
