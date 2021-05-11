(
    async () => {
        var apiData = await getApiData();
        var displayData = apiData.filter(d => d.country === 'Australia');
        console.log('displayData', displayData);
        var dates = displayData.map(o => o.date);
        console.log('dates', dates);
        var confirmed = displayData.map(o => o.confirmed);
        console.log('confirmed', confirmed);

        const button = document.getElementById('refreshButton');
        button.addEventListener("click", refresh);

        const ctx = document.getElementById('chart');
        var chart = new Chart(ctx, {

            type: 'bar',
            data: {
              labels: dates,
              datasets: [{
                label: displayData[0].country,
                backgroundColor: 'red',
                data: confirmed
              }]
            },

        });

        function refresh() {
            displayData = apiData.filter(d => d.country === document.getElementById("cname").value);
            console.log('displayData', displayData);
            dates = displayData.map(o => o.date);
            console.log('dates', dates);
            confirmed = displayData.map(o => o.confirmed);
            console.log('confirmed', confirmed);
            var newData = {
              labels: dates,
              datasets: [{
                label: displayData[0].country,
                backgroundColor: 'red',
                data: confirmed
              }]
            };
            chart.data = newData;
            chart.update();
        }

        async function getApiData() {
            const apiResult = await fetch("http://127.0.0.1:8000/vaccine_data_visual/covid_data");
            const json = await apiResult.json();
            return json;
        }

    }
)();

