var app = angular.module('WebInterfaceApp', [])

app.controller('AppController', function appCtrl($scope, $http){
    var Project = $resource('/project');
    $scope.projects = [{'title':'blah'}];


    Project.query(function(response){
        window.alert("GET");
        $scope.projects = response;
    });

});

app.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);