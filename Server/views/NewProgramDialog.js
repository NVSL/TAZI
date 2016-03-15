function NewProgramDialogController($scope, $mdDialog) {
    $scope.createNewProgram = function() {
        name = $scope.project.programName.toString();
        $.post("/newprogram", { "name" : name }, function(d) {
            if (d === "1")
                window.location = "/programs/" + name 
        });
        $mdDialog.hide();
      };
}

angular.module('dialogNewProgram', ['ngMaterial'])
  .controller('AppCtrl', function($scope, $mdDialog, $mdMedia) {
  $scope.status = '  ';
  $scope.customFullscreen = $mdMedia('xs') || $mdMedia('sm');
  $scope.createNewProgram = function() { 
      console.log($scope.project.programName); 
  };
  $scope.showNewProgramDialog = function(ev) {
    var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
    $mdDialog.show({
      controller: NewProgramDialogController,
      templateUrl: 'static/views/NewProgramDialog.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
      escapeToClose:true,
      fullscreen: useFullScreen
    });
    $scope.$watch(function() {
      return $mdMedia('xs') || $mdMedia('sm');
    }, function(wantsFullScreen) {
      $scope.customFullscreen = (wantsFullScreen === true);
    });
  };
});
