var app = angular.module('WebInterfaceApp', []);

app.config(function($interpolateProvider){
   $interpolateProvider.startSymbol('{[{');
   $interpolateProvider.endSymbol('}]}');
});


app.controller('ListCtrl', function ListCtrl($scope, $log, $http){

    $scope.siteCalibrationCheckbox = false;

    $scope.setMainContentState = function(state){
        $scope.mainContentState = state;
    }

    $scope.initialize = function(data){
        $scope.mainContentState = "INIT";
    };

    $scope.setCurrentProject = function(project){
        $scope.currProject = project;
    }

    $scope.loadSingleProject = function(projectTitle) {
            //This is causing two responses, 301 and 200, 200 is good, but the 300 says 'moved permanently' and lacks a /
            var project = $http.get('/api/v1/projects/' + projectTitle).then(function(response){
            $scope.setSideBarTitle(projectTitle);
            $scope.setCurrentProject(project);
            return response.data;
        });
    };

    $scope.loadProjects = function() {
            $scope.projects = $http.get('/api/v1/projects/').then(function(response){
            $scope.setSideBarTitle("Projects");
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
            $scope.setSideBarTitle(projectTitle);
            return response.data;
        });
    };


    $scope.setSideBarTitle = function(sideBarTitle){
        $scope.sideBarTitle = sideBarTitle;
    }

    $scope.setSideBarMode = function(sideBarMode){
        $scope.sideBarMode = sideBarMode;

        if(sideBarMode == "project-list"){
            $scope.setSideBarTitle("Projects");
            $scope.setCurrentProject(null);
        }else{
            $scope.setSideBarTitle("error?");
        }
    }

    $scope.setSideBarMode("project-list");


/*    $scope.createProject = function(form){
        var formData = {};
        formData["title"] = this.my_form.title["$modelValue"];
        //formData["hasSiteCalibration"] = this.my_form.siteCalibration["$modelValue"];

        $http.post('/api/v1/projects/', formData).then(function(){
            $scope.loadProjects();
            $scope.setMainContentState('project-view');
            $scope.loadSingleProject(formData["title"]);
            $scope.setSideBarMode('project-obj');
        });
    }*/


    $scope.createProject = function(title, sitecal) {
        window.alert(sitecal);

        $http.post('/api/v1/projects/', {
            title: title,
            site_calibration_allowed: sitecal
        }).then(function() {
            $scope.loadProjects();
            $scope.setMainContentState('project-view');
            $scope.loadSingleProject(title);
            $scope.setSideBarMode('project-obj');
        });
    }


    $scope.uploadSiteCalibration = function() {

    };

});