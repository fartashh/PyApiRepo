/**
 * Created by Fartash on 10/23/2014.
 */
/**
 * Created by Fartash on 10/21/2014.
 */


var app = angular.module('myApp')

app.controller("CredentialController", function ($rootScope, $scope, $http) {
    $scope.action = {};


    $scope.action.init = function () {

    }

    $scope.action.create_consumer_key = function () {
        if ($rootScope.user) {
            var data = {}
            data.user_id = $rootScope.user.id
            $http.get('/create_consumer_key', {
                params: { user_id: $rootScope.user.id }
            }).success(function (res) {
                console.log(res)

                for (i in res.result) {
                    $rootScope.user[i] = res.result[i]
                }
                console.log($rootScope.user)

            }).error(function (res) {

            })
        }
    }

    $scope.action.reset_consumer_key = function () {
        if ($rootScope.user) {
            var data = {}
            data.user_id = $rootScope.user.id
            $http.get('/reset_consumer_key', {
                params: { user_id: $rootScope.user.id }
            }).success(function (res) {

                for (i in res.result) {
                    $rootScope.user[i] = res.result[i]
                }

            }).error(function (res) {

            })
        }
    }


})