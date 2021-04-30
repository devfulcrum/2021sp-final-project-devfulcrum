(function(){
    'use strict';

    angular.module('vaccine_data_visual.demo', [])
        .controller('VaccineDataVisualController', [ '$scope', VaccineDataVisualController]);

    function VaccineDataVisualController($scope) {
        $scope.data = [
            {
                country: 'Australia',
                date: '2021-04-23',
                doses_administered: 5000
            },
            {
                country: 'India',
                date: '2021-04-23',
                doses_administered: 9000
            }
        ];
    }

}());
