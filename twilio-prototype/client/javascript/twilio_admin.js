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
    $scope.user = {};

    $scope.users = [];

    $http.get("/api/u").success(function(data) {
      //console.log(data);
      $scope.users = data;
    });
  }
]);

// Simple logging to make sure everything loaded correctly
console.log("Angular has been loaded!");
