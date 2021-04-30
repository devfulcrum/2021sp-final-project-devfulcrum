(function(){
    'use strict';

    angular.module('vaccine_data_visual.demo', [])
        .controller('VaccineDataVisualController', [ '$scope', '$http', VaccineDataVisualController]);

    function VaccineDataVisualController($scope, $http) {
        $scope.data = [];
        $http.get('/vaccine_data_visual/covid_data').then(function(response){
            $scope.data = response.data;
        });
    }

}());
