var tazi = angular.module('Tazi', ['ngMaterial']);
function CompilingDialogController($scope, $mdDialog, $mdToast) {
    var xml = getXML();
    $.post("/compile",  { "xml" : xml } , function(data) {
        console.log(data);
        $mdDialog.hide();
    });
}
tazi.controller('AppCtrl', function($scope, $mdDialog, $mdMedia, $mdToast) {
  $scope.status = '  ';
  $scope.customFullscreen = $mdMedia('xs') || $mdMedia('sm');
  $scope.createNewProgram = function() { 
      console.log($scope.project.programName); 
  };
  $scope.sendCompilePost = function(ev) { 
    var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
    $mdDialog
    .show({
      controller: CompilingDialogController,
      templateUrl: '/static/views/CompilingDialog.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      fullscreen: useFullScreen
    })
    .finally(function() {
	$scope.showToast("Running your program!")
    });
  };
  $scope.$watch(function() {
    return $mdMedia('xs') || $mdMedia('sm');
  }, function(wantsFullScreen) {
    $scope.customFullscreen = (wantsFullScreen === true);
  });
  // Toast Stuff
  var last = {
      bottom: true,
      top: false,
      left: false,
      right: true
  };
  $scope.toastPosition = angular.extend({},last);
  $scope.getToastPosition = function() {
    sanitizePosition();
    return Object.keys($scope.toastPosition)
      .filter(function(pos) { return $scope.toastPosition[pos]; })
      .join(' ');
  };
  function sanitizePosition() {
    var current = $scope.toastPosition;
    if ( current.bottom && last.top ) current.top = false;
    if ( current.top && last.bottom ) current.bottom = false;
    if ( current.right && last.left ) current.left = false;
    if ( current.left && last.right ) current.right = false;
    last = angular.extend({},current);
  }
  $scope.showToast = function( w ) {
    var pinTo = $scope.getToastPosition();
    $mdToast.show(
      $mdToast.simple()
        .textContent(w)
        .position(pinTo )
        .hideDelay(1000)
    );
  };
  // Post Requests in scope
  $scope.sendKillPost = function() {
      $scope.showToast("Stopping your program");
      $.post("/killprogram" ); 
  };
  $scope.sendSavePost = function() {
      $scope.showToast("Saving your program");
      $.post("/saveprogram",  { "xml" : getXML() } );
  };
  $scope.createNewProgram = function() { 
      console.log($scope.project.programName); 
  };
  $scope.runProgram = function() {
      $.post("/runprogram");
  };
});

