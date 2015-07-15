/**
 * Created by Fartash on 10/23/2014.
 */
/**
 * Created by Fartash on 10/21/2014.
 */
var app = angular.module('myApp')

app.controller("StatisticController", function ($rootScope, $scope, $http) {
    $scope.action = {};
    $scope.user = {
        table: [],
        chart: [
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
        $scope.action.get_usage_stat(1)
        $scope.action.drawChart($scope.user.chart)
    }


    $scope.action.get_usage_stat = function (page) {

        if ($rootScope.user) {

            var data = {user_id: $rootScope.user.id, page: page}
            $http.post('/get_usage_stat', JSON.stringify(data))
                .success(function (res) {
                    if (res.rescode == '00') {
                        $scope.user.table = res.result['table_data']
                        $scope.user.chart = res.result['chart_data']
                        $scope.action.drawChart($scope.user.chart)

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

    $scope.action.get_api_log = function (api_name) {

        if ($rootScope.user) {

            var data = {user_id: $rootScope.user.id, api_name: api_name}
            $http.post('/get_api_log', JSON.stringify(data))
                .success(function (res) {

                    var hiddenElement = document.createElement('a');

                    hiddenElement.href = 'data:attachment/csv,' + encodeURI(res);
                    hiddenElement.target = '_blank';
                    hiddenElement.download = api_name+'.csv';
                    hiddenElement.click();
                }).error(function (res) {
                })
        }

    }


})