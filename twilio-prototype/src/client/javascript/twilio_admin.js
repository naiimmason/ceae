var app = angular.module('twilio-admin', ['ngRoute', 'ngSanitize', 'ngCsv']);

// Configure routes for this application
app.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    $routeProvider.when('/', {
      templateUrl: '../html/partials/admin_home.html',
      controller: 'AdminController'
    })
    .when('/u/:id', {
      templateUrl: '../html/partials/user.html',
      controller: 'UserController'
    })
    .when('/p/:id', {
      templateUrl: '../html/partials/report_period.html',
      controller: 'PeriodController'
    })
    .when('/w/:id', {
      templateUrl: '../html/partials/meter.html',
      controller: 'MeterController'
    })
    .otherwise({
      redirectTo: '/'
    });
}]);

// This controls the user display page, grab the users and their messages
app.controller('UserController', ['$scope', '$routeParams', '$location', '$http',
  function($scope, $routeParams, $location, $http) {
    $scope.updating = false;
    $scope.messages = [];
    $scope.meters = [];
    $scope.user = {};

    $http.get('/api/u/id/' + $routeParams.id).success(function(data) {
      $scope.user = data;
    });

    $http.get('/api/u/id/' + $routeParams.id + '/m').success(function(data) {
      $scope.messages = data;
    });

    $http.get('/api/u/id/'  + $routeParams.id + '/w').success(function(data) {
      $scope.meters = data;
    });


    // Save the new user information and send it to the server via a put method
    $scope.saveUser = function() {
      var c = confirm('Do you wish to update this user\'s info?');

      if(c === true) {
        var options = {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        };
        console.log('Push new info to server!');
        $http.put('/api/u', transformRequest($scope.user), options).success(function(data) {
          console.log(data);
        });
        $scope.updating = false;
      } else {
        $scope.updating = false;
        $http.get('/api/u/id/' + $routeParams.id).success(function(data) {
          $scope.user = data;
          $scope.originaluser = data;
        });
      }
    };
  }
]);

// This controls the main admin screen where all the action happens
app.controller('AdminController', ['$scope', '$http', '$location',
  function($scope, $http, $location) {
    // Grab the admins info for funsies
    $scope.user = {};
    $http.get('/api/u/me').success(function(data) {
      $scope.user = data;
    });

    // REPORTING PERIOD
    $scope.show_reporting = false;
    $scope.newreport= {
      startDate: '',
      endDate: ''
    };

    $scope.add_report_string = 'Add Reporting Period';

    // Show/hide the reporting period addition form
    $scope.toggle_show_reporting = function() {
      $scope.show_reporting = !$scope.show_reporting;
      if($scope.show_reporting) {
        $scope.add_report_string = 'Cancel Adding';
      } else {
        $scope.add_report_string = 'Add Reporting Period';
        $scope.newreport.startDate = '';
        $scope.newreport.endDate = '';
      }
    };

    // Add the reporting period to the database based on the current user input
    $scope.start_reporting = function() {
      // For convience check and output the current date
      console.log(Date.now());
      if ($scope.newreport.startDate < Date.now() && $scope.newreport.endDate > Date.now()) {
        console.log('Now falls between that range');
      } else {
        console.log('You are not in range!');
      }

      // Because we have to user form urlencoded for twilio we must convert our json
      // objects into the type. Grab the information and convert then post
      var options = {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      };

      $http.post('/api/p', transformRequest($scope.newreport), options).success(function(data){
         console.log(data);
         $scope.newreport.startDate = '';
         $scope.newreport.endDate = '';
      });

      $scope.show_reporting = !$scope.show_reporting;
      $scope.add_report_string = 'Add Reporting Period';
    };

    // PERIOD LIST
    $scope.periods = [];
    $scope.show_periods = false;
    $scope.show_periods_string = 'Show Reporting Periods';

    $scope.toggle_show_periods = function() {
      $scope.show_periods = !$scope.show_periods;
      if($scope.show_periods) {
        $scope.show_periods_string = 'Hide Reporting Periods';
        $http.get('/api/p').success(function(data) {
          $scope.periods = [];
          $scope.periods = data;
          //console.log($scope.periods[0].startDate);
        });
      } else {
        $scope.show_periods_string = 'Show Reporting Periods';
      }
    };

    $scope.delete_period = function(index) {
      var c = confirm('Are you sure you want to delete this reporting period?');
      if(c === true) {
        $http.delete('/api/p/id/' + $scope.periods[index]._id).success(function(data) {
          console.log(data);

          $http.get('/api/p').success(function(data) {
            $scope.periods = data;
          });
        });
      }
    };

    // USER LIST
    // This code shows / hides the list of total users and updates the list
    $scope.show_users = false;
    $scope.show_users_string = 'Show';
    $scope.users = [];

    // Code to call upon click the show/hide users button
    $scope.toggle_show_users = function() {
      $http.get('/api/u').success(function(data) {
        $scope.users = data;
      });
      $scope.show_users = !$scope.show_users;
      if ($scope.show_users)
        $scope.show_users_string = 'Hide';
      else
        $scope.show_users_string = 'Show';
    };

    // ADD USER
    // Show / hide the add user interface
    $scope.show_add_cell = false;
    $scope.show_add_cell_string = 'Add Cell Number';
    $scope.newuser = {
      firstname: '',
      lastname: '',
      number: '',
      salutation: '',
      farmerid: '',
      contractType: ''
    };

    // code to call when clicking add cell button
    $scope.toggle_show_add_cell = function() {
      $scope.show_add_cell = !$scope.show_add_cell;
      if ($scope.show_add_cell)
        $scope.show_add_cell_string = 'Cancel Adding';
      else {
        $scope.show_add_cell_string = 'Add Cell Number';
        $scope.newuser.firstname = '';
        $scope.newuser.lastname = '';
        $scope.newuser.number = '';
      }
    };

    // send a post request to the api with all of the variables
    $scope.add_user = function() {
      $scope.show_add_cell = false;
      $scope.show_add_cell_string = 'Add Cell Number';
      console.log($scope.newuser);
      $scope.newuser.number = '+' + String($scope.newuser.number);

      var options = {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      };

      $http.post('/api/u', transformRequest($scope.newuser), options).success(function(data) {
        console.log(data);
        $scope.newuser.firstname = '';
        $scope.newuser.lastname = '';
        $scope.newuser.number = '';
        $scope.newuser.salutation = '';
        $scope.newuser.contractType = '';
        $scope.newuser.farmerid = '';
      });
    };

    // BROADCAST MESSAGE
    $scope.newmessage = {message: ''};
    $scope.show_broadcast = false;
    $scope.broadcast_btn_string = 'Broadcast Message';

    $scope.toggle_broadcast = function() {
      $scope.show_broadcast = !$scope.show_broadcast;
      if ($scope.show_broadcast)
        $scope.broadcast_btn_string = 'Cancel Broadcast';
      else {
        $scope.broadcast_btn_string = 'Broadcast Message';
        $scope.newmessage.message = '';
      }
    };

    $scope.broadcast_message = function() {
      $scope.show_broadcast = false;
      $scope.broadcast_btn_string = 'Broadcast Message';
      amessage = $scope.newmessage;

      var options = {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      };

      $http.post('/api/m/broadcast', transformRequest(amessage), options).success(function(data) {
        console.log(data);
        $scope.newmessage = '';
      });
    };

    // Delete a user from the user list
    $scope.delete_user = function(index) {
      var c = confirm('Are you sure you want to delete this user?');
      if(c === true) {
        $http.delete('/api/u/id/' + $scope.users[index]._id).success(function(data) {
          console.log(data);

          $http.get('/api/u').success(function(data) {
            $scope.users = data;
          });
        });
      }
    };
  }
]);

// Show the current period information
app.controller('PeriodController', ['$scope', '$http', '$location', '$routeParams', '$interval',
  function($scope, $http, $location, $routeParams, $interval) {
    $scope.messages = [];
    $scope.users = [];
    $scope.meters = [];
    $scope.period = '';
    $scope.seconds = 10;
    $scope.allowExport = false;
    $scope.exportArray = [{ a: 'Meter Serial Number', b: 'user database id', c: 'First Name',
      d: 'Last Name', e: 'Contract Type', f: 'Invite ID', g: 'Cell Number', h: 'Email',
      i: 'Payment Method', j: 'Bank', k: 'Meter Value', l: 'Date Submitted'}];

    // Grab the period information
    $http.get('/api/p/id/' + $routeParams.id).success(function(data) {
      console.log($scope.period);
      $scope.period = data;
    });

    // Grab all messages from that period
    $http.get('/api/p/id/' + $routeParams.id + '/m').success(function(data) {
      var tempexport = [];

      $scope.messages = data;

      $http.get('/api/p/id/' + $routeParams.id +  '/w').success(function(meters) {
        $scope.meters = meters;
        var tempusers = [];
        for(var j = 0, lenj = meters.length; j < lenj; j++) {
          //  console.log(meters[j]);
          $scope.exportArray.push({ a: meters[j].serialnumber, l: meters[j].user });
          if(tempusers.indexOf(meters[j].user) < 0) {
            tempusers.push(meters[j].user);
          }
        }

        for(j = 0, lenj = tempusers.length; j < lenj; j++) {
          $http.get('/api/u/id/' + tempusers[j]).success(function(data) {
            $scope.users.push(data);
            for(var k = 0; k < $scope.exportArray.length; k++) {
              if($scope.exportArray[k].l === data._id) {
                $scope.exportArray[k].c = data.firstname;
                $scope.exportArray[k].d = data.lastname;
                $scope.exportArray[k].e = data.contractType;
                $scope.exportArray[k].f = data.invitationid;
                $scope.exportArray[k].g = data.number;
                $scope.exportArray[k].h = data.email;
                $scope.exportArray[k].i = data.payment;
                $scope.exportArray[k].j = data.bank;

                for(var q = 0, lenq = $scope.messages.length; q < lenq; q++) {
                  if($scope.messages[q].invitationid === data.invitationid && $scope.messages[q].body.split(',')[0] === $scope.exportArray[k].a) {
                    console.log($scope.messages[q]);
                    $scope.exportArray[k].b = $scope.messages[q].body.split(',')[1];
                    $scope.exportArray[k].k = $scope.messages[q].date;
                  }
                }
              }
            }
          });
        }

        var timer = $interval(function(){
          console.log('hi');
          $scope.seconds -= 1;
          if($scope.seconds === 0) {

            $scope.allowExport = true;
            if (angular.isDefined(timer)) {
              $interval.cancel(timer);
              timer = undefined;
            }
          }
        }, 1000);
      });
    });
  }
]);

app.controller('MeterController', ['$scope', '$http', '$location', '$routeParams',
  function($scope, $http, $location, $routeParams) {
    $scope.meter = {};
    $scope.user = {};

    $http.get('/api/w/id/' + $routeParams.id).success(function(data) {
      $scope.meter = data;

      $http.get('/api/u/id/' + $scope.meter.user).success(function(data) {
        $scope.user = data;
      });
    });
  }
]);

// Transform a JSON objecct into a urlencoded object thing
function transformRequest(obj) {
  var str = [];
  for(var p in obj)
  str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p]));
  return str.join('&');
}

// Simple logging to make sure everything loaded correctly
console.log('Angular has been loaded!');
