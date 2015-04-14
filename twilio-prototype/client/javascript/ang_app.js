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
    .when("/admin", {
      templateUrl: "/html/partials/admin.html",
      controller: "AdminController"
    })
    .otherwise({
      redirectTo: "/"
    });
}]);

// This controll controls the home page!!!
// Doesn't really do anything, the home page should just be a static page
app.controller("HomeController", ["$scope", "$location", "$http",
  function($scope, $location, $http) {
  }
]);

app.controller("UserController", ["$scope", "$routeParams", "$location", "$http",
  function($scope, $routeParams, $location, $http) {
    $http.get("/api/u/me").success(function(data) {
      $scope.user = data
      if(!$scope.user.admin) {
        $location.path("/#/");
      }
    })

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

    $http.get("/api/u/me").success(function(data) {
      $scope.user = data
      if(!$scope.user.admin) {
        $location.path("/#/");
      }
    })

    $scope.users = [];

    $http.get("/api/u").success(function(data) {
      $scope.users = data;
    });
  }
]);

// Simple logging to make sure everything loaded correctly
console.log("Angular has been loaded!");
