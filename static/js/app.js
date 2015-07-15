/**
 * Created by Fartash on 10/20/2014.
 */




var app = angular.module('myApp', ['ngRoute','ngCookies','jsonFormatter','ngSanitize'])




app.directive('equals', function () {
    return {
        restrict: 'A', // only activate on element attribute
        require: '?ngModel', // get a hold of NgModelController
        link: function (scope, elem, attrs, ngModel) {
            if (!ngModel) return; // do nothing if no ng-model

            // watch own value and re-validate on change
            scope.$watch(attrs.ngModel, function () {

                validate();
            });

            // observe the other value and re-validate on change
            attrs.$observe('equals', function (val) {
                validate();
            });

            var validate = function () {
                // values
                var val1 = ngModel.$viewValue;
                var val2=''
                if(scope.signup_form===undefined){
                    val2 = scope.profile_form.password.$modelValue;
                }
                else{
                     val2 = scope.signup_form.password.$modelValue;
                }


                // set validity
                ngModel.$setValidity('equals', !val1 || !val2 || val1 === val2);
            };
        }
    }
});







app.config(['$routeProvider', function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'views/home.html',
            controller: 'HomeController'
        })
        .when('/signup', {
            templateUrl: 'views/signup.html',
            controller: 'SignupController'
        })
        .when('/console', {
            templateUrl: 'views/console.html',
            controller: 'ConsoleController'
        })
        .otherwise({redirectTo: '/'})
}]);








google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(function () {
    angular.bootstrap(document.body, ['myApp']);
});










