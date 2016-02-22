var app = angular.module('WebInterfaceApp', []);

app.config(function($interpolateProvider){
   $interpolateProvider.startSymbol('{[{');
   $interpolateProvider.endSymbol('}]}');
});


app.controller('ListCtrl', function ListCtrl($scope, $log, $http){

    $scope.initialize = function(data){
        $log.log('initialize', data);
        $scope.initData = data;
    };

    $scope.loadProjects = function() {
            $scope.projects = $http.get('/api/v1/projects/').then(function(response){
            return response.data;
        });
    };
    $scope.loadProjects();


    $scope.loadAnalyses = function() {
            $scope.analyses = $http.get('/api/v1/analyses/').then(function(response){
            return response.data;
        });
    };
    $scope.loadAnalyses();

    $scope.loadProjectAnalyses = function(projectTitle) {
            $scope.analyses = $http.get('/api/v1/project-analyses/' + projectTitle).then(function(response){
            return response.data;
        });
    };


    $scope.setSideBarMode = function(sideBarMode){
        $scope.sideBarMode = sideBarMode;
    }

    $scope.setSideBarMode("project-list");
});