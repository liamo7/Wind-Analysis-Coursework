var app = angular.module('webinterface', ['ngRoute', 'ngDialog', 'ngFileUpload', 'toaster', 'ngAnimate']);


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
            templateUrl: 'static/templates/analysis/detail.html'
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

        getAnalysis: function(projectTitle, analysisTitle) {
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

        getDataFiles: function (type, id) {
            return $http.post('/api/v1/datafiles/', {
                type: type,
                dataID: id
            });
        }

    };

});


app.controller('mainController', function($location, $http, $scope, projectService, toaster) {

    function init() {
        $scope.currentProject = null;
        $scope.selectedTurbine = null;
        $scope.sidebarType = 'projects';
        $scope.currentProject = null;
        $scope.currentAnalysis = null;
        $scope.combinedCols = null;
        $scope.plotTableData = null;

        getProjects();
        getTurbines();

        $location.path('/');
    } init();


    function closeAnalysis() {
        $scope.currentAnalysis = null;
        $scope.calculationRows = null;
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

    function getProjects() {
        projectService.all().then(function(response) {
            $scope.projectList = response.data;
        });
    }


    function getTurbines() {
        projectService.turbines().then(function(response) {
            $scope.turbineList = response.data;
        });
    }

    function getProject(title) {
        projectService.getProject(title).then(function (response) {
            $scope.currentProject = response.data;
        })
    }


    function getAnalysis(title) {
        projectService.getAnalysis(title).then(function (response) {
            $scope.currentProject = response.data;
        })
    }

    $scope.loadAnalysis = function(analysis) {
        $scope.currentAnalysis = analysis;
        getAnalyses($scope.currentProject.title);
        setSidebarType('analysisOpened');
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
                    getProjects();
                    $scope.loadProject(response.config.data);
                    $location.path('/project/' + title + '/files/upload');
                    toaster.pop('success', response.data.success)
                }
                else {
                    toaster.pop('error', response.data.error);
                }
            });
        }
    };

    $scope.createTurbine = function(name, bin, powerInKillowats, isValid) {

        if (isValid) {
            return $http.post('/api/v1/turbines/', {
                name: name,
                bin: JSON.parse(bin),
                powerInKillowats: JSON.parse(powerInKillowats)
            }).then(function (response) {
                if (response.data.success) {
                    toaster.pop('success', response.data.success);
                } else {
                    toaster.pop('error', response.data.error);
                }
            });
        }
    };

    projectService.getColumnTypes().then(function(response) {
        $scope.columnTypes = response.data;
    });

    projectService.getValueTypes().then(function(response) {
        $scope.valueTypes = response.data;
    });


    function getAnalyses(title) {
        projectService.getAnalyses(title).then(function(response) {
            $scope.analysesList = response.data;

            if($scope.currentAnalysis != null) {
                for(var x=0; x<$scope.analysesList.length; x++) {;
                    if($scope.currentAnalysis.title == $scope.analysesList[x].title) {
                        setSidebarType('analysisOpened');
                        $scope.currentAnalysis = $scope.analysesList[x];
                        console.log($scope.currentAnalysis);

                        if($scope.currentAnalysis.analysisType == 1) {
                            projectService.getDataFiles('calculation', $scope.currentAnalysis['id']).then(function (response) {
                                $scope.calculationRows = response.data;
                            });
                        }
                    }
                }
            }

        });
    }

    $scope.loadProject = function(project) {

        getProject(project.title);
        setSidebarType('projectOpened');
        getAnalyses(project.title);
    };

    $scope.imageExists = function(image, object, index) {
        var img = new Image();
        img.onload = function() {
          object[index] = true;
          $scope.$apply();
        };
        img.onerror = function() {
          return false;
        };
        img.src = image;
     };
});


app.controller('projectCreationController', function ($location, $http, $scope, ngDialog, projectService, Upload, toaster) {

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
                if(response.data.success) {
                    $scope.combinedCols = response.data.combinedCols;
                    toaster.pop('success', response.data.success);
                    $location.path('/project/' + $scope.currentProject.title + '/');
                } else {
                    toaster.pop('error', response.data.error);
                    $scope.progressPercentage = 0;
                }
            }, function (response) {
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
            };

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

app.controller('analysisCreationController', function ($location, $http, $scope, ngDialog, projectService, toaster) {

    function init() {
        $scope.columnNames = [];
        $scope.syncedFile = null;
        $scope.dataFiles = {1: 'Synchronised', 2: 'Derived'};
        $scope.derivedDataFiles = [];
        $scope.addedPlots = {};
        $scope.plotCount = 0;

        //Table related

        $scope.calculationTypes = {'airDensity': 'airDensity', 'turbulenceIntensity': 'turbulenceIntensity', 'windShearExponentPolyfit': 'windShearExponentPolyfit',
            'twoHeightWindShearExponent': 'twoHeightWindShearExponent', 'wind_direction_bin': 'wind_direction_bin', 'siteCorrectedWindSpeed': 'siteCorrectedWindSpeed', 'normalisedWindSpeed': 'normalisedWindSpeed',
            'windSpeedBin': 'windSpeedBin', 'hubHeightSpecificEnergyProduction': 'specificEnergyProduction', 'powerDeviation': 'powerDeviation'};

        $scope.kwargTypes = ['string', 'float', 'function', 'checkbox'];

        $scope.calculationRows = {};

        $scope.selectedColumns = [];
        $scope.selectedKwargs = {};
        $scope.selectedCalculation = null;
        $scope.selectedColumnType = null;
        $scope.tableCount = 0;

        console.log("INIT");

    } init();

    projectService.getDataFiles('combined', $scope.currentProject['id']).then(function (response) {
        $scope.combinedCols = response.data.combinedFileCols;
        $scope.combinedCols.push.apply($scope.combinedCols, Object.keys($scope.calculationTypes));
        $scope.derivedDataFiles.push(response.data.derivedDataAnalyses);
        $scope.dataFiles = response.data.derivedDataAnalyses;
        $scope.dataFiles[1] = 'Synchronised';

        console.log($scope.dataFiles);
    });

    $scope.addCalculation = function (calc) {
        projectService.getProject($scope.currentProject.title).then(function(response) {
            $scope.currentProject = response.data;

        });
        
    };

    $scope.addColumn = function(col) {
        if($scope.selectedColumns.indexOf(col) == -1)
            $scope.selectedColumns.push(col);
    };
    
    $scope.addKwarg = function(key, value) {

        $scope.selectedKwargs[key] = value;

    };

    $scope.removeTableRow = function (row) {
        delete $scope.calculationRows[row];
    };

    $scope.addTableRow = function(calcType, cols, colType, kwargs) {

        $scope.tableCount++;

        $scope.calculationRows['row' + $scope.tableCount] = {};
        $scope.calculationRows['row' + $scope.tableCount].calcType = $scope.calculationTypes[calcType];
        $scope.calculationRows['row' + $scope.tableCount]['cols'] = cols;
        $scope.calculationRows['row' + $scope.tableCount]['colTypeString'] = colType;
        $scope.calculationRows['row' + $scope.tableCount]['colType'] = $scope.columnTypes.indexOf(colType);
        $scope.calculationRows['row' + $scope.tableCount]['kwargs'] = kwargs;

        $scope.selectedColumns = [];
        $scope.selectedKwargs = {};
        $scope.selectedCalculation = null;
        $scope.selectedColumnType = null;

    };

    $scope.removePlotRow = function (row) {
        delete $scope.addedPlots[row];
    };

    $scope.fillTable = function () {
      
        $scope.calculationRows['row1'] = {};
        $scope.calculationRows['row1'].calcType = $scope.calculationTypes['airDensity'];
        $scope.calculationRows['row1']['cols'] = ['Pressure (mBar)', 'Temperature (C)', 'Relative humidity (%)'];
        $scope.calculationRows['row1']['colTypeString'] = 'AIR_DENSITY';
        $scope.calculationRows['row1']['colType'] = $scope.columnTypes.indexOf('AIR_DENSITY');
        $scope.calculationRows['row1']['kwargs'] = {};

        $scope.calculationRows['row2'] = {};
        $scope.calculationRows['row2'].calcType = $scope.calculationTypes['turbulenceIntensity'];
        $scope.calculationRows['row2']['cols'] = ['Mast - 80m Wind Speed Mean', 'Mast - 80m Wind Speed Std Dev'];
        $scope.calculationRows['row2']['colTypeString'] = 'TURBULENCE_INTENSITY';
        $scope.calculationRows['row2']['colType'] = $scope.columnTypes.indexOf('TURBULENCE_INTENSITY');
        $scope.calculationRows['row2']['kwargs'] = {};

        $scope.calculationRows['row3'] = {};
        $scope.calculationRows['row3'].calcType = $scope.calculationTypes['twoHeightWindShearExponent'];
        $scope.calculationRows['row3']['cols'] = ['Mast - 64m Wind Speed Mean', 'Mast - 80m Wind Speed Mean'];
        $scope.calculationRows['row3']['colTypeString'] = 'WIND_SHEAR_EXPONENT';
        $scope.calculationRows['row3']['colType'] = $scope.columnTypes.indexOf('WIND_SHEAR_EXPONENT');
        $scope.calculationRows['row3']['kwargs'] = {'lowerHeight': 64, 'upperHeight': 80};

        $scope.calculationRows['row4'] = {};
        $scope.calculationRows['row4'].calcType = $scope.calculationTypes['wind_direction_bin'];
        $scope.calculationRows['row4']['cols'] = ['Mast - 82m Wind Direction Mean'];
        $scope.calculationRows['row4']['colTypeString'] = 'DERIVED';
        $scope.calculationRows['row4']['colType'] = $scope.columnTypes.indexOf('DERIVED');
        $scope.calculationRows['row4']['kwargs'] = {'binWidth': 10};

        $scope.calculationRows['row5'] = {};
        $scope.calculationRows['row5'].calcType = $scope.calculationTypes['siteCorrectedWindSpeed'];
        $scope.calculationRows['row5']['cols'] = ['Mast - 80m Wind Speed Mean', 'wind_direction_bin'];
        $scope.calculationRows['row5']['colTypeString'] = 'DERIVED';
        $scope.calculationRows['row5']['colType'] = $scope.columnTypes.indexOf('DERIVED');
        $scope.calculationRows['row5']['kwargs'] = {'factors': 'siteCalibrationFactors'};

        $scope.calculationRows['row6'] = {};
        $scope.calculationRows['row6'].calcType = $scope.calculationTypes['normalisedWindSpeed'];
        $scope.calculationRows['row6']['cols'] = ['siteCorrectedWindSpeed', 'airDensity'];
        $scope.calculationRows['row6']['colTypeString'] = 'WIND_SPEED';
        $scope.calculationRows['row6']['colType'] = $scope.columnTypes.indexOf('WIND_SPEED');
        $scope.calculationRows['row6']['kwargs'] = {};

        $scope.calculationRows['row7'] = {};
        $scope.calculationRows['row7'].calcType = $scope.calculationTypes['windSpeedBin'];
        $scope.calculationRows['row7']['cols'] = ['normalisedWindSpeed'];
        $scope.calculationRows['row7']['colTypeString'] = 'DERIVED';
        $scope.calculationRows['row7']['colType'] = $scope.columnTypes.indexOf('DERIVED');
        $scope.calculationRows['row7']['kwargs'] = {'binWidth': 0.5, 'zeroIsBinStart': false};

        $scope.calculationRows['row8'] = {};
        $scope.calculationRows['row8'].calcType = $scope.calculationTypes['hubHeightSpecificEnergyProduction'];
        $scope.calculationRows['row8']['cols'] = [];
        $scope.calculationRows['row8']['colTypeString'] = 'DERIVED';
        $scope.calculationRows['row8']['colType'] = $scope.columnTypes.indexOf('DERIVED');
        $scope.calculationRows['row8']['kwargs'] = {'windSpeedColumn': 'normalisedWindSpeed', 'powerCurve': 'warrantedPowerCurve'};

        $scope.calculationRows['row9'] = {};
        $scope.calculationRows['row9'].calcType = $scope.calculationTypes['powerDeviation'];
        $scope.calculationRows['row9']['cols'] = ['Power mean (kW)', 'normalisedWindSpeed'];
        $scope.calculationRows['row9']['colTypeString'] = 'DERIVED';
        $scope.calculationRows['row9']['colType'] = $scope.columnTypes.indexOf('DERIVED');
        $scope.calculationRows['row9']['kwargs'] = {'powerCurve': 'warrantedPowerCurve'};

    };
    
    $scope.fillPlots = function () {
        $scope.addedPlots['plot1'] = {};
        $scope.addedPlots['plot1'].plotType = 'Distribution';
        $scope.addedPlots['plot1'].cols = ['Power mean (kW)', 'powerDeviation'];
        
        $scope.addedPlots['plot2'] = {};
        $scope.addedPlots['plot2'].plotType = 'PowerCurve';
        $scope.addedPlots['plot2'].cols = ['normalisedWindSpeed', 'Power mean (kW)'];
    };

    $scope.addPlot = function (plotType, cols, data) {
        $scope.plotCount++;
        $scope.addedPlots['plot' + $scope.plotCount] = {};
        $scope.addedPlots['plot' + $scope.plotCount].plotType = plotType;
        $scope.addedPlots['plot' + $scope.plotCount].cols = cols;

        $scope.selectedColumns = [];
    };

    $scope.createAnalysis = function(title, project, calculations, analysisType, plotTypes) {
        if($scope.currentProject != null) {
            return $http.post('/api/v1/analyses/', {
                title: title,
                calculations: calculations,
                project: project,
                typeAnalysis: analysisType,
                plotTypes: plotTypes
            }).then(function (response) {
                if (response.data.success) {
                    $scope.loadAnalysis(response.config.data);
                    $location.path('/project/' + project.title + '/' + title);
                    toaster.pop('success', response.data.success);
                    //$scope.plotTableData = JSON.parse(response.data.plotData);
                    var s = response.data.plotData;
                    $scope.plotTableData = {'mean': 43, 'max': 32};
                } else {
                    toaster.pop('error', response.data.error);
                }
            });
        }
    };
});


