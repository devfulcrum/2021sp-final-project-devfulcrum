(
    async () => {
        var apiData = await getApiData();
        var displayData = apiData.filter(d => d.country === 'Australia');
        console.log('displayData', displayData);
        var dates = displayData.map(o => o.date);
        console.log('dates', dates);
        var doses = displayData.map(o => o.doses_administered);
        console.log('doses', doses);

        const button = document.getElementById('refreshButton2');
        button.addEventListener("click", refresh);

        const ctx = document.getElementById('chart2');
        var chart = new Chart(ctx, {

            type: 'bar',
            data: {
              labels: dates,
              datasets: [{
                label: displayData[0].country,
                backgroundColor: 'green',
                data: doses
              }]
            },

        });

        function refresh() {
            displayData = apiData.filter(d => d.country === document.getElementById("cname2").value);
            console.log('displayData', displayData);
            dates = displayData.map(o => o.date);
            console.log('dates', dates);
            doses = displayData.map(o => o.doses_administered);
            console.log('doses', doses);
            var newData = {
              labels: dates,
              datasets: [{
                label: displayData[0].country,
                backgroundColor: 'green',
                data: doses
              }]
            };
            chart.data = newData;
            chart.update();
        }

        async function getApiData() {
            const apiResult = await fetch("http://127.0.0.1:8000/vaccine_data_visual/vaccine_data");
            const json = await apiResult.json();
            return json;
        }

    }
)();

