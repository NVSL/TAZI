var tazi = angular.module('Tazi', ['ngMaterial']);
function CompilingDialogController($scope, $mdDialog) {
    var xml = getXML();
    $.post("/compile",  { "xml" : xml } , function(data) {
        console.log(data);
        $mdDialog.hide();
          //alert(data);
    });
}
tazi.controller('AppCtrl', function($scope, $mdDialog, $mdMedia) {
  $scope.status = '  ';
  $scope.customFullscreen = $mdMedia('xs') || $mdMedia('sm');
  $scope.createNewProgram = function() { 
      console.log($scope.project.programName); 
  };
  $scope.sendCompilePost = function(ev) { 
    var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
    $mdDialog.show({
      controller: CompilingDialogController,
      templateUrl: '/static/views/CompilingDialog.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      fullscreen: useFullScreen
    });
  };
  $scope.$watch(function() {
    return $mdMedia('xs') || $mdMedia('sm');
  }, function(wantsFullScreen) {
    $scope.customFullscreen = (wantsFullScreen === true);
  });
  // Post Requests
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
