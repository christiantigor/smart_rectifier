var haApp = angular.module('haApp', [ 'nvd3', 'ngAria', 'ngMessages',
		'ngAnimate', 'ngMaterial', 'ngRoute', 'haControllers', 'haServices',
		'ngMaterialDatePicker', 'md.data.table' ]);

haApp.config([
		'$routeProvider',
		'$mdThemingProvider',
		function($routeProvider, $mdThemingProvider) {
			$mdThemingProvider.theme('default').primaryPalette('teal')
					.accentPalette('red');

			$routeProvider.when('/main', {
				templateUrl : 'partials/main.html',
				controller : 'MainCtrl'
			}).otherwise({
				redirectTo : '/main'
			});
		} ]);

haApp.directive('confirmationDialog', [ function() {
	return {
		restrict : 'E',
		scope : {
			haMessage : '@',
			haConfirmed : '&',
			haDialogModel : '=',
			haDialogId : '@haDialogModel'
		},
		templateUrl : 'snippets/confirmation.html',
		link : function($scope, element, attrs) {
			$scope.$watch('haDialogModel', function(value) {
				if (value) {
					$scope.obj = value;
					$scope.obj.show = function() {
						$('#' + $scope.haDialogId).modal('show');
					};
					console.log($scope.haMessage);
				}
			}, true);
		}
	};
} ]);