/**
 * Created by Fartash on 10/23/2014.
 */
/**
 * Created by Fartash on 10/21/2014.
 */


var app = angular.module('myApp')

app.controller("CreditController", function ($rootScope, $scope, $http) {
    $scope.action = {};
    $scope.credit = {
        amount: 0.00,
        reports: [],
        requested_amount: 0.00
    }
    $scope.selcted_page=1

    $scope.action.init = function () {
        $scope.action.load_credit(1)
    }

    $scope.action.credit_request = function () {
        if ($rootScope.user) {

            var data = {user_id: $rootScope.user.id, amount: parseFloat($scope.credit.requested_amount)}
            $http.post('/credit_request', JSON.stringify(data))
                .success(function (res) {
                    console.log(res)
                    if (res.rescode == '00') {
                        if ($scope.credit_form) $scope.credit_form.$setPristine();
                        $scope.action.load_credit(1)
                    }
                    else {
                    }
                }).error(function (res) {
                })
        }
    }

    $scope.action.load_credit = function (page) {
        $scope.selcted_page=page
        if ($rootScope.user) {

            var data = {user_id: $rootScope.user.id, page: page}
            $http.post('/load_credit', JSON.stringify(data))
                .success(function (res) {
                    if (res.rescode == '00') {
                        $scope.credit = res.result
                    }
                    else {
                    }
                }).error(function (res) {
                })
        }
    }


    $scope.action.getNumber = function (num) {
        var result = [];
        for (var i = 1; i <= Math.ceil(num); i++) {
            result.push(i);
        }
        return result;
    }


})