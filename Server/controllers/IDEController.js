var tazi = angular.module('Tazi', ['ngMaterial']);
tazi.controller('AppCtrl', function($scope, $mdDialog, $mdMedia) {
  $scope.status = '  ';
  $scope.customFullscreen = $mdMedia('xs') || $mdMedia('sm');
  $scope.createNewProgram = function() { 
      console.log($scope.project.programName); 
  };
  // Post Requests
  $scope.sendCompilePost = function() { 
      testPost();
  };
  $scope.sendKillPost = function() {
      sendKillSignal();
  };
  $scope.createNewProgram = function() { 
      console.log($scope.project.programName); 
  };
  $scope.runProgram = function() {
      $.post("/runprogram");
  };
});
