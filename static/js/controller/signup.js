/**
 * Created by Fartash on 10/21/2014.
 *
 * ora-kit puchong
 */

var app = angular.module('myApp')


app.controller("SignupController", function ($rootScope, $scope, $http, $location) {
    $scope.clicked=false
    $scope.action = {}
    $rootScope.user_model = {}

    $scope.signup_message = ''


    $scope.action.signup = function () {
        $scope.clicked=true
        $http.post('/signup', JSON.stringify($scope.signup))
            .success(function (res) {
                console.log(res)
                if (res.rescode == '00') {
                    $location.path("/home")
                }
                else {
                    $scope.signup_message = "* " + res.res_message
                }
            }).error(function (res) {
                $scope.signup_message = "* UnExpected Error"
            })
    }

})