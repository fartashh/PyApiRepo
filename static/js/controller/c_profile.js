/**
 * Created by Fartash on 10/23/2014.
 */
/**
 * Created by Fartash on 10/21/2014.
 */
var app = angular.module('myApp')

app.controller("ProfileController", function ($rootScope, $scope, $http) {
    $scope.action = {};

    $scope.data = {
        chart: [
            ['date', 'app1', 'app2'],
            ['Oct 17', 0.0000, 0.0000],
            ['Oct 17', 0.0000, 0.0000],
            ['Oct 17', 0.0000, 0.0000],
            ['Oct 17', 0.0000, 0.0000],
            ['Oct 17', 0.0000, 0.0000],
            ['Oct 17', 0.0000, 0.0000],
            ['Oct 17', 0.0000, 0.0000]
        ]
    }
$scope.profile_message = ''

    $scope.action.init = function () {
        if ($rootScope.user) {
            $scope.profile = $rootScope.user
            $scope.profile.password=''
            $scope.profile.repassword=''
        }

    }



        $scope.action.update_profile = function () {
        $http.post('/signup', JSON.stringify($scope.profile))
            .success(function (res) {
                console.log(res)
                if (res.rescode == '00') {
                    $scope.clicked=true
                    $scope.profile_message = 'Your profile successfully updated'

                }
                else {
                    $scope.signup_message = "* " + res.res_message
                }
            }).error(function (res) {
                $scope.signup_message = "* UnExpected Error"
            })
    }





})