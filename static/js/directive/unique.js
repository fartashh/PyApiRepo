/**
 * Created by Fartash on 10/21/2014.
 */

var app = angular.module('myApp')


app.directive('ensureUnique', ['$http', '$timeout', function ($http, $timeout) {
    var checking = null;
    return {
        require: 'ngModel',
        link: function (scope, ele, attrs, c) {
            scope.$watch(attrs.ngModel, function (newVal) {
                if (!checking) {
                    checking = $timeout(function () {
                        var data = {}
                        data.filed = attrs.ensureUnique
                        data.value = newVal
                        $http.post('/check_uniqueness', JSON.stringify(data)).success(function (data, status, headers, cfg) {
                            if (data.rescode == "00") {

                                c.$setValidity('unique', true);
                                checking = null;
                            }
                            else {
                                c.$setValidity('unique', false);
                                checking = null;
                            }
                        }).error(function (data, status, headers, cfg) {
                            checking = null;
                        });
                    }, 500);
                }
            });
        }
    }
}]);
