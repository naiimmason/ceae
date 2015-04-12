var app = angular.module("twilio-prototype", ["ngRoute"]);

// Configure routes for this application
app.config(["$routeProvider", "$locationProvider", 
  function($routeProvider, $locationProvider) {
    $routeProvider.when("/", {
      templateUrl: "/html/partials/home.html",
      controller: "HomeController"
    })
    .when("/u/:id", {
      templateUrl: "/html/partials/user.html",
      controller: "UserController"
    })
    .otherwise({
      redirectTo: "/"
    });
}]);

// This controll controls the home page!!!
app.controller("HomeController", ["$scope", "$location", "$http",
  function($scope, $location, $http) {
    $scope.users = [];
    $http.get("/api/u").success(function(data) {
      $scope.users = data;
    });
  }
]);

app.controller("UserController", ["$scope", "$routeParams", "$http",
  function($scope, $routeParams, $http) {
    $scope.messages = [];
    $scope.user = {};
    $http.get("/api/u/" + $routeParams.id).success(function(data) {
      $scope.user = data;
    });

    $http.get("/api/u/" + $routeParams.id + "/m").success(function(data) {
      $scope.messages = data;
    });
  }
]);

// Simple logging to make sure everything loaded correctly
console.log("Angular has been loaded!");
