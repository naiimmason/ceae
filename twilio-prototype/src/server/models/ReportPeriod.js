var mongoose = require("mongoose");
var Schema = mongoose.Schema;

var reportPeriodSchema = new Schema({
  startDate: Date,
  endDate: Date
});

module.exports = mongoose.model("ReportPeriod", reportPeriodSchema);
