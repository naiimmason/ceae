var app = angular.module('signup', []);

app.controller('SignupController', ['$scope', '$http', '$window',
  function($scope, $http, $window) {

    $scope.submitted = false;
    // Stock meters array to show template and to initialize with at least one
    // meter
    $scope.meters=[{
      'serialnumber': '',
      'meterUnits': '.1',
      'acresIrrigated': '',
      'crops': [{
        'type': '',
        'acres': ''
      }]
    }];

    // New user object that stores all of their information
    $scope.newuser = {
      'invitationid': '',
      'lastname': '',
      'firstname': '',
      'salutation': 'Mr.',
      'areacode': '',
      'firstthree': '',
      'lastfour': '',
      'payment': 'paypal',
      'eamil': ''
    };

    $scope.checknum = {
      'areacode': '',
      'firstthree': '',
      'lastfour': ''
    };

    // Add a new meter to the list of meters and check to make sure that they
    // only add 5 meters
    $scope.addMeter = function() {
      if($scope.meters.length < 5) {
        $scope.meters.push({
          'serialnumber': '',
          'meterUnits': '.1',
          'acresIrrigated': '',
          'crops': [{
            'type': '',
            'acres': ''
          }]});
      } else {
        alert('You may only register a maximum of 5 meters.');
      }
    };

    // Delete a meter from a specific index
    $scope.deleteMeter = function(index) {
      if($scope.meters.length > 1) {
        var c = confirm('Are you sure you wish to delete this meter?');
        if(c) {
          $scope.meters.splice(index, 1);
        }
      } else {
        alert('You must register at least one water meter!');
      }
    };

    // Add a new crop to a specific meter
    $scope.addCrop = function(index) {
      $scope.meters[index].crops.push({ type: '', acres: '' });
    };

    // Delete a crop
    $scope.deleteCrop = function(meterIndex, cropIndex) {
      $scope.meters[meterIndex].crops.splice(cropIndex, 1);
    };

    $scope.addUser = function() {
      $scope.submitted = true;

      var options = {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      };

      $scope.newuser.number = '+1' + $scope.newuser.areacode + '' + $scope.newuser.firstthree + '' + $scope.newuser.lastfour;

      $http.post('/api/u', transformRequest($scope.newuser), options).success(function(data) {
        console.log(data);

        for(var i = 0, len = $scope.meters.length; i < len; i++) {
          var ameter = $scope.meters[i];
          ameter.user = data._id;
          ameter.crops = '';

          for(var j = 0, lenj = $scope.meters[i].crops.length; j < lenj; j++) {
            ameter.crops += $scope.meters[i].crops[j].type + ': ' + ameter[j].acres + ', ';
          }

          $http.post('/api/w', transformRequest(ameter), options).success(function(anothermeter) {
            console.log(anothermeter);
          });
        }
      });
    };
  }
]);

app.directive('sameAs', function() {
  return {
    require: 'ngModel',
    link: function(scope, elem, attrs, ngModel) {
      ngModel.$parsers.unshift(validate);

      // Force-trigger the parsing pipeline.
      scope.$watch(attrs.sameAs, function() {
          ngModel.$setViewValue(ngModel.$viewValue);
      });

      function validate(value) {
          var isValid = scope.$eval(attrs.sameAs) == value;

          ngModel.$setValidity('same-as', isValid);

          return isValid ? value : undefined;
      }
    }
  };
});

// Transform a JSON objecct into a urlencoded object thing
function transformRequest(obj) {
  var str = [];
  for(var p in obj)
  str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p]));
  return str.join('&');
}
