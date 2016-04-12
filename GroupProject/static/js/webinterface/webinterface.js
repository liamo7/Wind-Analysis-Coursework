var app = angular.module('webinterface', ['ngRoute', 'ngDialog', 'ngFileUpload']);


app.config(function($locationProvider, $interpolateProvider, $routeProvider, $httpProvider) {

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix("!");

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');

    //If you pass 'controller: mainController' in routeProvider,
    //it calls a new controller reseting all variables.
    //Should move to multiple controllers though instead of big global mess
    $routeProvider

        .when('/', {
            templateUrl: '/static/templates/project/list.html'
        })

        .when('/project/create', {
            templateUrl: '/static/templates/project/create.html'
        })

        .when('/project/:title/update', {
            templateUrl: '/static/templates/project/update.html'
        })

        .when('/project/:title/files/upload', {
            templateUrl: '/static/templates/project/fileupload.html'
        })

        .when('/project/:title', {
            templateUrl: '/static/templates/project/detail.html'
        })

        .when('/project/:title/:analysis', {
            templateUrl: 'static/templates/test.html'
        })

        .when('/turbine/create', {
            templateUrl: '/static/templates/turbine/create.html'
        })

        .when('/project/analysis/analysis/create', {
            templateUrl: '/static/templates/analysis/create.html'
        });
});


//Services allow communication between controller functionality
//eg get project list
app.factory('projectService', function($http, $routeParams) {


    return {
        all: function() {
            return $http.get('/api/v1/projects/');
        },

        get: function() {
            return $http.get('/api/v1/projects/' + $routeParams.title + '/');
        },

        getAnalyses: function(projectTitle) {
            return $http.get('/api/v1/analyses/' + projectTitle + '/');
        },

        getAnalysis: function(analysisTitle) {
            return $http.get('/api/v1/analyses/' + projectTitle + '/');
        },

        turbines: function() {
            return $http.get('/api/v1/turbines/');
        },

        getColumnTypes: function() {
            return $http.get('/api/v1/columntypes/');
        },

        getValueTypes: function() {
            return $http.get('/api/v1/valuetypes/');
        }
    };

});


app.controller('mainController', function($location, $http, $scope, projectService) {

    function init() {
        console.log("init");
        $scope.currentProject = null;
        $scope.selectedTurbine = null;
        $scope.sidebarType = null;
        $scope.currentProject = null;
        $scope.currentAnalysis = null;
        $location.path('/');
    } init();


    function closeAnalysis() {
        $scope.currentAnalysis = null;
        $location.path('/project/' + $scope.currentProject.title);
    };

    //without () = assigns but doesnt call
    $scope.closeProject = init
    $scope.closeAnalysis = closeAnalysis;

    function setSidebarType(type) {
        switch (type) {
            case 'projects':
                $scope.sidebarType = type;
                window.alert(type);
                break;

            case 'turbines':
                $scope.sidebarType = type;
                break;

            case 'projectOpened':
                $scope.sidebarType = type;
                break;
        }
    }

    function setCurrentProject(project) {
        $scope.currentProject = project;
    }

    function setCurrentAnalysis(analysis) {
        $scope.currentAnalysis = analysis;
    }
    projectService.all().then(function(response) {
        $scope.projectList = response.data;
    });

    projectService.turbines().then(function(response) {
        $scope.turbineList = response.data;
    });

    $scope.loadAnalysis = function(analysis) {
        setCurrentAnalysis(analysis);
    }

    $scope.loadProject = function(project) {
        setCurrentProject(project);
        setSidebarType('projectOpened');

        projectService.getAnalyses(project.title).then(function(response) {
            $scope.analysesList = response.data;
        });
    };

    $scope.createProject = function(title, description, turbine) {

        projectService.getColumnTypes();


        return $http.post('/api/v1/projects/', {
            title: title,
            description: description,
            turbine: JSON.parse(turbine)
        }).then(function (response) {
            $scope.loadProject(response.config.data);
            $location.path('/project/' + title);
        });
    };

    $scope.createAnalysis = function(title, project) {
        if($scope.currentProject != null) {
            return $http.post('/api/v1/analyses/', {
                title: title,
                project: project
            });
        }
    };

    $scope.createTurbine = function(name, bin, powerInKillowats) {
        return $http.post('/api/v1/turbines/', {
            name: name,
            bin: JSON.parse(bin),
            powerInKillowats: JSON.parse(powerInKillowats),

        });
    };


});


app.controller('projectCreationController', function ($location, $http, $scope, ngDialog, projectService, Upload) {

    function init() {
        console.log("init project controller");
        $scope.columnNames = null;
        $scope.fileType = null;

        $scope.mastFileDict = {};
        $scope.lidarFileDict = {};
        $scope.powerFileDict = {};

    } init();

    $scope.uploadFiles = function(mastFile, lidarFile, powerFile) {
        Upload.upload({
                url: '/api/v1/projects/' + $scope.currentProject.title + '/',
                data: {
                    powerFileDict: $scope.powerFileDict,
                    powerFile: powerFile,
                    mastFile: mastFile,
                    mastFileDict: $scope.mastFileDict,
                    lidarFile: lidarFile,
                    lidarFileDict: $scope.lidarFileDict,
                    projectTitle: $scope.currentProject.title,
                },
                method: 'put'
            }).then(function (resp) {
                console.log('Success uploaded. Response: ' + resp.data);
        });
    };

    $scope.fileNameChanged = function (input) {
        $scope.fileType = input.id;
        var file = input.files[0];
        $scope.fileData = {};

        var reader = new FileReader();
        reader.onload = function (e) {
            var fileContents = e.target.result;
            var columnHeaders = fileContents.split('\n')[0].split('\t');
            columnHeaders.splice(0, 1);
            $scope.columnNames = columnHeaders;

            for(var x=0; x<$scope.columnNames.length; x++) {
                $scope.fileData['col' + x] = {};
                $scope.fileData['col' + x].name = $scope.columnNames[x];
                $scope.fileData['col' + x].positionInFile = x + 1;
            }

            ngDialog.openConfirm({
                    template: '/static/templates/project/selectHeaders.html',
                    scope: $scope, //Pass the scope object if you need to access in the template
                }).then(
                function (value) {

                    for(var key in $scope.fileData) {
                        //starts at zero - we need to add 1 for the enums
                        $scope.fileData[key].columnType = $scope.columnTypes.indexOf($scope.fileData[key].columnType) + 1;
                        $scope.fileData[key].valueType = $scope.valueTypes.indexOf($scope.fileData[key].valueType) + 1;

                        if($scope.fileData[key].toUse == false)
                            delete $scope.fileData[key]
                    }


                    switch ($scope.fileType) {
                        case 'mastFile':
                            $scope.mastFileDict = JSON.stringify($scope.fileData);
                            alert($scope.mastFileDict);
                            console.log($scope.mastFileDict);
                            break;

                        case 'lidarFile':
                            $scope.lidarFileDict = JSON.stringify($scope.fileData);
                            alert($scope.lidarFileDict);
                            console.log($scope.lidarFileDict);
                            break;

                        case 'powerFile':
                            $scope.powerFileDict = JSON.stringify($scope.fileData);
                            alert($scope.powerFileDict);
                            console.log($scope.powerFileDict);
                            break;
                    }

                },

                function (value) {

                //Cancel
                });
            };

        reader.readAsText(file);

        };

    projectService.getColumnTypes().then(function(response) {
        $scope.columnTypes = response.data;
    });

    projectService.getValueTypes().then(function(response) {
        $scope.valueTypes = response.data;
    });

});

app.controller('analysisCreationController', function ($location, $http, $scope, ngDialog) {

    function init() {
        console.log("init analysis controller");
        $scope.selectedProcess = null;
        $scope.processes = {};
        $scope.processParams = ['param1', 'param2', 'param3'];
        $scope.columnNames = ['col1', 'col2', 'col3'];

        $scope.selectedColumns = [];
    }

    init();

    $scope.addProcess = function (process) {
        alert(JSON.stringify(process, null, 4));
        var key = Object.keys(process)[0];
        $scope.processes[key] = process[key];
        $scope.selectedProcess = null;
    };

    $scope.loadFunctionParams = function () {
        // TODO load the function params from the server and set processParams to them
    };

    $scope.showPrompt = function () {
        ngDialog.close();

        $scope.loadFunctionParams($scope.selectedProcess);

        ngDialog.openConfirm({
            template: '/static/templates/analysis/createProcess.html',
            scope: $scope
        }).then(
            function (value) {
                //save the contact form
                var process = {};
                process[$scope.selectedProcess] = [$scope.selectedColumns];
                $scope.addProcess(process);
            },
            function (value) {
                //Cancel or do nothing
                $scope.processParams = {};
            });

    };

});



