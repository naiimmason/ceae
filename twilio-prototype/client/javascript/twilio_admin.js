var app = angular.module("twilio-admin", ["ngRoute"]);

// Configure routes for this application
app.config(["$routeProvider", "$locationProvider",
  function($routeProvider, $locationProvider) {
    $routeProvider.when("/", {
      templateUrl: "/html/partials/admin_home.html",
      controller: "AdminController"
    })
    .when("/u/:id", {
      templateUrl: "/html/partials/user.html",
      controller: "UserController"
    })
    .otherwise({
      redirectTo: "/"
    });
}]);

app.controller("UserController", ["$scope", "$routeParams", "$location", "$http",
  function($scope, $routeParams, $location, $http) {
    $scope.messages = [];
    $scope.user = {};
    $http.get("/api/u/id/" + $routeParams.id).success(function(data) {
      $scope.user = data;
    });

    $http.get("/api/u/id/" + $routeParams.id + "/m").success(function(data) {
      $scope.messages = data;
    });
  }
]);

app.controller("AdminController", ["$scope", "$http", "$location",
  function($scope, $http, $location) {
    // Grab the admins info for funsies
    $scope.user = {};
    $http.get("/api/u/me").success(function(data) {
      $scope.user = data;
    });

    // REPORTING PERIOD
    $scope.show_reporting = false;
    $scope.newreport= {
      startDate: "",
      endDate: ""
    };

    $scope.toggle_show_reporting = function() {
      $scope.show_reporting = !$scope.show_reporting;
    };

    $scope.start_reporting = function() {
      console.log(Date.now());
      if ($scope.newreport.startDate < Date.now() && $scope.newreport.endDate > Date.now()) {
        console.log("Now falls between that range");
      } else {
        console.log("You are not in range!");
      }

      var options = {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      };

      $http.post("/api/p", transformRequest($scope.newreport), options).success(function(data){
         console.log(data);
      });
    };

    // USER LIST
    // This code shows / hides the list of total users and updates the list
    $scope.show_users = false;
    $scope.show_users_string = "Show";
    $scope.users = [];

    // Code to call upon click the show/hide users button
    $scope.toggle_show_users = function() {
      $http.get("/api/u").success(function(data) {
        $scope.users = data;
      });
      $scope.show_users = !$scope.show_users;
      if ($scope.show_users)
        $scope.show_users_string = "Hide";
      else
        $scope.show_users_string = "Show";
    };

    // ADD USER
    // Show / hide the add user interface
    $scope.show_add_cell = false;
    $scope.show_add_cell_string = "Add Cell Number";

    // code to call when clicking add cell button
    $scope.toggle_show_add_cell = function() {
      $scope.show_add_cell = !$scope.show_add_cell;
      if ($scope.show_add_cell)
        $scope.show_add_cell_string = "Cancel Adding";
      else {
        $scope.show_add_cell_string = "Add Cell Number";
        // $scope.newuser.firstname = "";
        // $scope.newuser.lastname = "";
        // $scope.newuser.number = "";
      }
    };

    $scope.newuser = {
      firstname: "",
      lastname: "",
      number: ""
    };

    // send a post request to the api with all of the variables
    $scope.add_user = function() {
      $scope.show_add_cell = false;
      $scope.show_add_cell_string = "Add Cell Number";
      console.log($scope.newuser);
      $scope.newuser.number = "+" + String($scope.newuser.number);

      var options = {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      };

      $http.post("/api/u", transformRequest($scope.newuser), options).success(function(data) {
        console.log(data);
      });
      // $scope.newuser.firstname = "";
      // $scope.newuser.lastname = "";
      // $scope.newuser.number = "";
    };

    // BROADCAST MESSAGE
    $scope.newmessage = {message: ""};
    $scope.show_broadcast = false;
    $scope.broadcast_btn_string = "Broadcast Message";

    $scope.toggle_broadcast = function() {
      $scope.show_broadcast = !$scope.show_broadcast;
      if ($scope.show_broadcast)
        $scope.broadcast_btn_string = "Cancel Broadcast";
      else {
        $scope.broadcast_btn_string = "Broadcast Message";
        $scope.newmessage.message = "";
      }
    };

    $scope.broadcast_message = function() {
      $scope.show_broadcast = false;
      $scope.broadcast_btn_string = "Broadcast Message";
      amessage = $scope.newmessage;

      var options = {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      };

      $http.post("/api/m/broadcast", transformRequest(amessage), options).success(function(data) {
        console.log(data);
      });
    };
  }
]);

function transformRequest(obj) {
  var str = [];
  for(var p in obj)
  str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
  return str.join("&");
}

// Simple logging to make sure everything loaded correctly
console.log("Angular has been loaded!");
