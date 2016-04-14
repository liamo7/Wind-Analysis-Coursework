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

        getProject: function (projectTitle) {
            return $http.get('/api/v1/projects/' + projectTitle + '/');
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
        },

    };

});


app.controller('mainController', function($location, $http, $scope, projectService) {

    function init() {
        $scope.currentProject = null;
        $scope.selectedTurbine = null;
        $scope.sidebarType = 'projects';
        $scope.currentProject = null;
        $scope.currentAnalysis = null;
        $location.path('/');
    } init();


    function closeAnalysis() {
        $scope.currentAnalysis = null;
        setSidebarType('projectOpened');
        $location.path('/project/' + $scope.currentProject.title);
    };

    //without () = assigns but doesnt call
    $scope.closeProject = init
    $scope.closeAnalysis = closeAnalysis;

    function setSidebarType(type) {
        switch (type) {
            case 'projects':
                $scope.sidebarType = type;
                break;

            case 'turbines':
                $scope.sidebarType = type;
                break;

            case 'projectOpened':
                $scope.sidebarType = type;
                break;

            case 'analysisOpened':
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
        setSidebarType('analysisOpened');
    }

    $scope.loadProject = function(project) {
        setCurrentProject(project);
        setSidebarType('projectOpened');

        projectService.getAnalyses(project.title).then(function(response) {
            $scope.analysesList = response.data;
        });
    };

    $scope.createProject = function(projectTitle, projectDescription, projectTurbine, isValid) {


        if(isValid) {
            projectService.getColumnTypes();

            $http.post('/api/v1/projects/', {
                title: projectTitle,
                description: projectDescription,
                turbine: JSON.parse(projectTurbine)
            }).then(function (response) {
                if (response.data.success) {
                    $scope.loadProject(response.config.data);
                    $location.path('/project/' + title + '/files/upload');
                }
                else {
                    $scope.error = response.data.error;
                }
            });
        }
    };

    $scope.createAnalysis = function(title, project) {
        if($scope.currentProject != null) {
            return $http.post('/api/v1/analyses/', {
                title: title,
                project: project
            }).then(function(response){
                alert(response);
                $scope.loadAnalysis(response.config.data);
                $location.path('/project/' + project.title + '/' + title);
            }, function errorCallback(response) {
                alert(response);
            });
        }
    };

    $scope.createTurbine = function(name, bin, powerInKillowats, isValid) {

        if(isValid) {
            return $http.post('/api/v1/turbines/', {
                name: name,
                bin: JSON.parse(bin),
                powerInKillowats: JSON.parse(powerInKillowats)
            }).then(function successCallback(response) {
                // this callback will be called asynchronously
                // when the response is available
            }, function errorCallback(response) {
                alert(response);
            });
        }
    };

    projectService.getColumnTypes().then(function(response) {
        $scope.columnTypes = response.data;
    });

    projectService.getValueTypes().then(function(response) {
        $scope.valueTypes = response.data;
    });
});


app.controller('projectCreationController', function ($location, $http, $scope, ngDialog, projectService, Upload) {

    function init() {
        $scope.columnNames = null;
        $scope.progressPercentage = 0;
        $scope.fileType = null;

        $scope.mastFileDict = {};
        $scope.lidarFileDict = {};
        $scope.powerFileDict = {};

        $scope.anemometersCols = [];

    } init();


    $scope.fillMast = function fillMast() {

         $scope.fileData['col0'].columnType = "WIND_DIRECTION";
         $scope.fileData['col0'].valueType = "MEAN";
         $scope.fileData['col0'].measurementHeight = 82.0;
         $scope.fileData['col0'].instrumentCalibrationSlope = 0.04577;
         $scope.fileData['col0'].instrumentCalibrationOffset = 0.2653;
         $scope.fileData['col0'].dataLoggerCalibrationSlope = 1.0;
         $scope.fileData['col0'].dataLoggerCalibrationOffset = 0.0;

         $scope.fileData['col1'].columnType = "WIND_SPEED";
         $scope.fileData['col1'].valueType = "MEAN";
         $scope.fileData['col1'].measurementHeight = 80.0;
         $scope.fileData['col1'].instrumentCalibrationSlope = 0.04581;
         $scope.fileData['col1'].instrumentCalibrationOffset = 0.2638;
         $scope.fileData['col1'].dataLoggerCalibrationSlope = 1.0;
         $scope.fileData['col1'].dataLoggerCalibrationOffset = 0.0;

         $scope.fileData['col2'].columnType = "WIND_SPEED";
         $scope.fileData['col2'].valueType = "STANDARD_DEVIATION";
         $scope.fileData['col2'].measurementHeight = 80.0;
         $scope.fileData['col2'].instrumentCalibrationSlope = 0.04577;
         $scope.fileData['col2'].instrumentCalibrationOffset = 0.2688;
         $scope.fileData['col2'].dataLoggerCalibrationSlope = 1.0;
         $scope.fileData['col2'].dataLoggerCalibrationOffset = 0.0;

         $scope.fileData['col3'].columnType = "WIND_SPEED";
         $scope.fileData['col3'].valueType = "MEAN";
         $scope.fileData['col3'].measurementHeight = 64.0;
         $scope.fileData['col3'].instrumentCalibrationSlope = 0.04583;
         $scope.fileData['col3'].instrumentCalibrationOffset = 0.2621;
         $scope.fileData['col3'].dataLoggerCalibrationSlope = 1.0;
         $scope.fileData['col3'].dataLoggerCalibrationOffset = 0.0;

         $scope.fileData['col4'].columnType = "WIND_SPEED";
         $scope.fileData['col4'].valueType = "MEAN";
         $scope.fileData['col4'].measurementHeight = 35.0;
         $scope.fileData['col4'].instrumentCalibrationSlope = 0.04581;
         $scope.fileData['col4'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col4'].dataLoggerCalibrationSlope = 0.0462;
         $scope.fileData['col4'].dataLoggerCalibrationOffset = 0.0;

         $scope.fileData['col5'].columnType = "PRESSURE";
         $scope.fileData['col5'].valueType = "MEAN";
         $scope.fileData['col5'].measurementHeight = 30.0;
         $scope.fileData['col5'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col5'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col5'].dataLoggerCalibrationSlope = 1.0;
         $scope.fileData['col5'].dataLoggerCalibrationOffset = 0.0;

         $scope.fileData['col6'].columnType = "RELATIVE_HUMIDITY";
         $scope.fileData['col6'].valueType = "MEAN";
         $scope.fileData['col6'].measurementHeight = 30.0;
         $scope.fileData['col6'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col6'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col6'].dataLoggerCalibrationSlope = 1.0;
         $scope.fileData['col6'].dataLoggerCalibrationOffset = 0.0;

         $scope.fileData['col7'].columnType = "TEMPERATURE";
         $scope.fileData['col7'].valueType = "MEAN";
         $scope.fileData['col7'].measurementHeight = 30.0;
         $scope.fileData['col7'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col7'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col7'].dataLoggerCalibrationSlope = 1.0;
         $scope.fileData['col7'].dataLoggerCalibrationOffset = 0.0;

    };

    $scope.fillLidar = function fillLidar() {

         $scope.fileData['col0'].columnType = "WIND_SPEED";
         $scope.fileData['col0'].valueType = "MEAN";
         $scope.fileData['col0'].measurementHeight = 132.5;
         $scope.fileData['col0'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col0'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col0'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col0'].dataLoggerCalibrationSlope = 1.0;

         $scope.fileData['col1'].columnType = "WIND_SPEED";
         $scope.fileData['col1'].valueType = "MEAN";
         $scope.fileData['col1'].measurementHeight = 127.5;
         $scope.fileData['col1'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col1'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col1'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col1'].dataLoggerCalibrationSlope = 1.0;

         $scope.fileData['col2'].columnType = "WIND_SPEED";
         $scope.fileData['col2'].valueType = "MEAN";
         $scope.fileData['col2'].measurementHeight = 117.5;
         $scope.fileData['col2'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col2'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col2'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col2'].dataLoggerCalibrationSlope = 1.0;

         $scope.fileData['col3'].columnType = "WIND_SPEED";
         $scope.fileData['col3'].valueType = "MEAN";
         $scope.fileData['col3'].measurementHeight = 107.5;
         $scope.fileData['col3'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col3'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col3'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col3'].dataLoggerCalibrationSlope = 1.0;

         $scope.fileData['col4'].columnType = "WIND_SPEED";
         $scope.fileData['col4'].valueType = "MEAN";
         $scope.fileData['col4'].measurementHeight = 97.5;
         $scope.fileData['col4'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col4'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col4'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col4'].dataLoggerCalibrationSlope = 1.0;

         $scope.fileData['col5'].columnType = "WIND_SPEED";
         $scope.fileData['col5'].valueType = "MEAN";
         $scope.fileData['col5'].measurementHeight = 87.5;
         $scope.fileData['col5'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col5'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col5'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col5'].dataLoggerCalibrationSlope = 1.0;

         $scope.fileData['col6'].columnType = "WIND_SPEED";
         $scope.fileData['col6'].valueType = "MEAN";
         $scope.fileData['col6'].measurementHeight = 77.5;
         $scope.fileData['col6'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col6'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col6'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col6'].dataLoggerCalibrationSlope = 1.0;

         $scope.fileData['col7'].columnType = "WIND_SPEED";
         $scope.fileData['col7'].valueType = "MEAN";
         $scope.fileData['col7'].measurementHeight = 67.5;
         $scope.fileData['col7'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col7'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col7'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col7'].dataLoggerCalibrationSlope = 1.0;

         $scope.fileData['col8'].columnType = "WIND_SPEED";
         $scope.fileData['col8'].valueType = "MEAN";
         $scope.fileData['col8'].measurementHeight = 57.5;
         $scope.fileData['col8'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col8'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col8'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col8'].dataLoggerCalibrationSlope = 1.0;

         $scope.fileData['col9'].columnType = "WIND_SPEED";
         $scope.fileData['col9'].valueType = "MEAN";
         $scope.fileData['col9'].measurementHeight = 42.5;
         $scope.fileData['col9'].instrumentCalibrationOffset = 0.0;
         $scope.fileData['col9'].instrumentCalibrationSlope = 1.0;
         $scope.fileData['col9'].dataLoggerCalibrationOffset = 0.0;
         $scope.fileData['col9'].dataLoggerCalibrationSlope = 1.0;
    };

    $scope.fillPower = function fillPower() {
        $scope.fileData['col0'].columnType = 'POWER';
        $scope.fileData['col0'].valueType = 'MEAN';
        $scope.fileData['col0'].measurementHeight = 82.0;
        $scope.fileData['col0'].instrumentCalibrationOffset = 0.0;
        $scope.fileData['col0'].instrumentCalibrationSlope = 1.0;
        $scope.fileData['col0'].dataLoggerCalibrationOffset = 0.0;
        $scope.fileData['col0'].dataLoggerCalibrationSlope = 1.0;;
    }


    $scope.uploadFiles = function(mastFile, lidarFile, powerFile, siteCalibration) {
        Upload.upload({
                url: '/api/v1/projects/' + $scope.currentProject.title + '/',
                data: {
                    siteCalibrationFile: siteCalibration,
                    powerFileDict: $scope.powerFileDict,
                    powerFile: powerFile,
                    mastFile: mastFile,
                    mastFileDict: $scope.mastFileDict,
                    lidarFile: lidarFile,
                    lidarFileDict: $scope.lidarFileDict,
                    projectTitle: $scope.currentProject.title,
                },
                method: 'put'
            }).then(function (response) {
                alert("success")
                $location.path('/project/' + $scope.currentProject.title + '/');
            }, function (response) {
                alert("Error");
            }, function (event) {
                $scope.progressPercentage = parseInt(100.0 * event.loaded / event.total);
        });
    };

    $scope.fileNameChanged = function (input) {
        $scope.fileType = input.id;
        var file = input.files[0];
        $scope.fileData = {};

        $scope.fileData['colSets'] = {
                'label': 'anemometers',
                'columnSet': ['Mast - 80m Wind Speed Mean', 'Mast - 64m Wind Speed Mean', 'Mast - 35.0m Wind Speed Mean']
            }

        var reader = new FileReader();
        reader.onload = function (e) {
            var fileContents = e.target.result;
            var columnHeaders = fileContents.split('\n')[0].split('\t');
            columnHeaders[columnHeaders.length-1] = columnHeaders[columnHeaders.length-1].replace('\r', '');
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
                        if(key != "colSets") {
                            $scope.fileData[key].columnType = $scope.columnTypes.indexOf($scope.fileData[key].columnType) + 1;
                            $scope.fileData[key].valueType = $scope.valueTypes.indexOf($scope.fileData[key].valueType) + 1;
                        }

                        if($scope.fileData[key].toUse == false)
                            delete $scope.fileData[key]
                    }


                    switch ($scope.fileType) {
                        case 'mastFile':
                            $scope.mastFileDict = JSON.stringify($scope.fileData);
                            break;

                        case 'lidarFile':
                            $scope.lidarFileDict = JSON.stringify($scope.fileData);
                            break;

                        case 'powerFile':
                            $scope.powerFileDict = JSON.stringify($scope.fileData);
                            break;
                    }

                },

                function (value) {

                //Cancel
                });
            };

        reader.readAsText(file);

        };

});

app.controller('analysisCreationController', function ($location, $http, $scope, ngDialog, projectService) {

    function init() {
        $scope.selectedProcess = null;
        $scope.processes = {};
        $scope.processParams = ['param1', 'param2', 'param3'];
        $scope.columnNames = ['col1', 'col2', 'col3'];

        $scope.syncedFile = null;

        $scope.calculationRows = [];

        $scope.selectedColumns = [];
    } init();

    $scope.addCalculation = function (calc) {
        projectService.getProject($scope.currentProject.title).then(function(response) {
            $scope.currentProject = response.data;
            console.log($scope.currentProject);

        });
        
    };


    $scope.addProcess = function (process) {
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
            template: '/static/templates/analysis/selectCalculations.html',
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


