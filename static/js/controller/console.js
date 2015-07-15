/**
 * Created by Fartash on 10/21/2014.
 */
var app = angular.module('myApp')

app.controller("ConsoleController", function ($rootScope, $scope, $http, $location, $cookieStore) {




    $scope.active_control={
        name:'overview',
        address:'views/controls/overview.html'

    }



//    $scope.active_control = "overview"



//    $scope.control = "views/controls/overview.html"
    $scope.action = {};

    $scope.action.init = function () {

        if ($rootScope.auth) {
            load_menu()
        }
        else {
            $location.path('/')
        }
    }

    $scope.action.load_control = function (control) {
        $scope.active_control.name = control
        $scope.active_control.address= "views/controls/" + control + '.html'
    }

    $scope.action.logout = function () {
        $cookieStore.remove('user_id')
        $location.path('/')
    }






})