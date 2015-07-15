/**
 * Created by Fartash on 10/23/2014.
 */
/**
 * Created by Fartash on 10/21/2014.
 */
var app = angular.module('myApp')

app.controller("DevlabController", function ($rootScope, $scope, $http) {
    $scope.methods = [
        ["GET", "GET"],
        ["POST", "POST"],
        ["PUT", "PUT"],
        ["DELETE", "DELETE"]
    ]

    $scope.response = {}


    $scope.action = {};

    $scope.response;
    $scope.request = {
        method: "GET",
        data: ''
    }


    $scope.action.init = function () {
        if($rootScope.user.apis)
            $rootScope.user.apis=$rootScope.user.apis.filter(function(e){return e[2]==true})

    }

    $scope.action.submit = function () {
        params={}
        p=$scope.action.parse_data($scope.request.data.split('?')[1])

        if(p['undefined']!="")
            params = p
        params['user_id'] = $rootScope.user.id
        params['consumer_key'] = $rootScope.user.consumer_key



        api_name=($scope.request.api===undefined || $scope.request.api==null)?'':$scope.request.api
        $http({
            method: $scope.request.method,

            url: "/api/"+api_name + $scope.request.data.split('?')[0],
            params: params
        }).success(function (res) {
            $scope.response = res
        }).error(function (res) {
            $scope.response = {'error': true}
        })


    }

    $scope.action.parse_data = function (data) {
        var match,
            pl = /\+/g,  // Regex for replacing addition symbol with a space
            search = /([^&=]+)=?([^&]*)/g,
            decode = function (s) {
                return decodeURIComponent(s.replace(pl, " "));
            },
            query = data;

        urlParams = {};
        while (match = search.exec(query))
            urlParams[decode(match[1])] = decode(match[2]);

        return urlParams
    }


})