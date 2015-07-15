/**
 * Created by Fartash on 10/23/2014.
 */
/**
 * Created by Fartash on 10/21/2014.
 */
var app = angular.module('myApp')

app.controller("OverviewController", function ($rootScope, $scope, $http) {
    $scope.action = {};

    $scope.data={
        chart:[
            ['', 'No API'],
            ['', 0.0000],
            ['', 0.0000],
            ['', 0.0000],
            ['', 0.0000],
            ['', 0.0000],
            ['', 0.0000],
            ['', 0.0000]
        ]
    }


    $scope.action.init = function () {
        $scope.action.get_user_info()
        $scope.action.drawChart($scope.data.chart)
        $scope.action.get_usage_stat(1)
    }


    $scope.action.get_user_info = function () {
        if ($rootScope.user) {
            var data = {}
            data.user_id = $rootScope.user.id
            $http.get('/get_user_info', {
                params: { user_id: $rootScope.user.id }
            }).success(function (res) {

                $rootScope.user = res.result
            }).error(function (res) {

            })
        }
    }

    $scope.action.get_usage_stat = function (page) {

        if ($rootScope.user) {

            var data = {user_id: $rootScope.user.id, page: page}
            $http.post('/get_usage_stat', JSON.stringify(data))
                .success(function (res) {
                    if (res.rescode == '00') {
                        $scope.data.chart = res.result['chart_data']

                        console.log($scope.data.chart)

                        $scope.action.drawChart($scope.data.chart)

                    }
                    else {
                    }
                }).error(function (res) {
                })
        }

    }

    $scope.action.drawChart = function (data) {

        var data = google.visualization.arrayToDataTable(data);
        var options = {
            width: '1352',
            vAxis: {title: 'Requests/sec'},
            legend: { position: 'bottom', alignment: 'start'},
            animation: {duration: 1000, easing: 'out'}
        };
        var chart = new google.visualization.LineChart(document.getElementById('chartdiv'));

        chart.draw(data, options);

    }


})