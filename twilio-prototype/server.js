server = require('./src/server/app.js');

// Start the server (taken from Andy which is taken from Cloud9)
server.listen(process.env.PORT || 3100, process.env.IP || "0.0.0.0", function() {
  var address = server.address();
  console.log("Server is now started on ", address.address + ":" + address.port);
});
