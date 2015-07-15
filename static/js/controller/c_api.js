/**
 * Created by Fartash on 10/23/2014.
 */
/**
 * Created by Fartash on 10/21/2014.
 */


var app = angular.module('myApp')

app.controller("ApiController", function ($rootScope, $scope, $http) {
    $scope.action = {};
    $scope.apis = []


    $scope.action.init = function () {
        $scope.action.load_apis()



    }

    $scope.action.load_apis = function () {
        if ($rootScope.user) {
            var data = {}
            $http.get('/load_apis').success(function (res) {
                $scope.apis = res.result


            }).error(function (res) {

            })
        }
    }

    $scope.action.manage_api = function (id, name,title) {
        if ($rootScope.user) {
            if (!$rootScope.user.apis)
                $rootScope.user.apis = []



            exist = false
            for (var i = 0; i < $rootScope.user.apis.length; ++i) {


                if ($rootScope.user.apis[i][0] == id && $rootScope.user.apis[i][2] == true) {
                    exist = true;
                    break;
                }
            }


            if (!exist) {
                $http.get('/manage_api', {params: { api_id: id, api_name: name, user_id: $rootScope.user.id, api_title:title}}).success(function (res) {
                    if (res.rescode == '00') {

                        inx = null
                        for (var i = 0; i < $rootScope.user.apis.length; ++i) {
                            if ($rootScope.user.apis[i][0] == id) {
                                inx=i
                                $rootScope.user.apis[i][2] = true;
                                break;
                            }
                        }
                        if(inx==null)
                            $rootScope.user.apis.push([id, name, true,title])
                    }

                }).error(function (res) {
                })
            }
            else {
                $http.delete('/manage_api', {params: { api_id: id, api_name: name, user_id: $rootScope.user.id, api_title:title}}).success(function (res) {
                    inx = null
                    for (var i = 0; i < $rootScope.user.apis.length; ++i) {
                        if ($rootScope.user.apis[i][0] == id) {
//                            inx = i;
                            $rootScope.user.apis[i][2] = false;


                            break;
                        }
                    }
//                    if (inx != null)
//                        $rootScope.user.apis.splice(inx, 1)

                }).error(function (res) {
                })
            }

        }
    }

    $scope.action.check = function (id) {
        if ($rootScope.user && $rootScope.user.apis) {
            res = $.grep($rootScope.user.apis, function (e) {
                return e[0] == id && e[2] == true
            })
            if (res.length == 0)
                return false
            else
                return true
        }
        else {
            return false
        }
    }

    $scope.action.readme = function (name) {

        $rootScope.modal = {
            header: name,
            body: ''
        }

        $http.get('/api_readme',
            {params: {  api_name: name}}
        ).success(function (res) {
                if (res.rescode == '00') {
                    //var w = window.open('')
                    $scope.modal.body = res.result
                }

            })
            .error(function (res) {
            })
    }


})