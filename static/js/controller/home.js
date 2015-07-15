/**
 * Created by Fartash on 10/21/2014.
 */


var app = angular.module('myApp')

app.controller("HomeController", function ($rootScope, $scope, $http, $location, $cookieStore) {
    $scope.action = {}
    $scope.signin_message = ''
    $rootScope.user = {id:''}
    $rootScope.auth = false


    $scope.action.init = function () {

        if($cookieStore.get('user_id')){
            $rootScope.user.id=$cookieStore.get('user_id')
            $rootScope.auth = true
            $location.path('/console')
        }

    }


    $scope.action.signin = function () {

        $http.post('/signin', JSON.stringify($scope.signin))
            .success(function (res) {

                if (res.rescode == '00') {
                    $rootScope.user = res.result
                    if($scope.signin.remember){
                        $cookieStore.put('user_id',res.result.id)
                    }
                    $rootScope.auth = true
                    $location.path('/console')


                }
                else {
                    $scope.signin_message = 'Invalid Username or Password'
                }

            })
            .error(function (res) {
                $scope.signin_message = 'Invalid Username or Password'
            })


    }


})
