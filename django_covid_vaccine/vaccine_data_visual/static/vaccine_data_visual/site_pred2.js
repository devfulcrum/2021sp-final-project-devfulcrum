(
    async () => {
        var apiData = await getApiData();
        console.log('apiData', apiData)
        var displayData = apiData.country_predict_doses.filter(d => d[3] === 'Australia');
        console.log('displayData', displayData)

        const button = document.getElementById('refreshButton4');
        button.addEventListener("click", refresh);

        const ctx = document.getElementById('chart4');
        var chart = new Chart(ctx, {

            type: 'bar',
            data: {
              labels: ["Day 1", "Day 2", "Day 3"],
              datasets: [
                  {
                    label: "Day 1",
                    backgroundColor: 'green',
                    data: displayData[0]
                  },
                  {
                    label: "Day 2",
                    backgroundColor: 'green',
                    data: displayData[1]
                  },
                  {
                    label: "Day 3",
                    backgroundColor: 'green',
                    data: displayData[2]
                  },
              ]
            },

        });

        function refresh() {
            displayData = apiData.country_predict_doses.filter(d => d[3] === document.getElementById("cname4").value);
            console.log('displayData', displayData);
            var newData = {
              labels: ["Day 1", "Day 2", "Day 3"],
              datasets: [
                  {
                    label: "Day 1",
                    backgroundColor: 'green',
                    data: displayData[0]
                  },
                  {
                    label: "Day 2",
                    backgroundColor: 'green',
                    data: displayData[1]
                  },
                  {
                    label: "Day 3",
                    backgroundColor: 'green',
                    data: displayData[2]
                  },
              ]
            };
            chart.data = newData;
            chart.update();
        }

        async function getApiData() {
            const apiResult = await fetch("http://127.0.0.1:8000/vaccine-doses-predict/");
            const json = await apiResult.json();
            return json;
        }

    }
)();

