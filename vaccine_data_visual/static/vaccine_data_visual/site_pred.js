(
    async () => {
        var apiData = await getApiData();
        console.log('apiData', apiData)
        var displayData = apiData.country_predict_cases.filter(d => d[3] === 'Australia');
        console.log('displayData', displayData)

        const button = document.getElementById('refreshButton3');
        button.addEventListener("click", refresh);

        const ctx = document.getElementById('chart3');
        var chart = new Chart(ctx, {

            type: 'bar',
            data: {
              labels: ["Day 1", "Day 2", "Day 3"],
              datasets: [
                  {
                    label: "Day 1",
                    backgroundColor: 'red',
                    data: displayData[0]
                  },
                  {
                    label: "Day 2",
                    backgroundColor: 'red',
                    data: displayData[1]
                  },
                  {
                    label: "Day 3",
                    backgroundColor: 'red',
                    data: displayData[2]
                  },
              ]
            },

        });

        function refresh() {
            displayData = apiData.country_predict_cases.filter(d => d[3] === document.getElementById("cname3").value);
            console.log('displayData', displayData);
            var newData = {
              labels: ["Day 1", "Day 2", "Day 3"],
              datasets: [
                  {
                    label: "Day 1",
                    backgroundColor: 'red',
                    data: displayData[0]
                  },
                  {
                    label: "Day 2",
                    backgroundColor: 'red',
                    data: displayData[1]
                  },
                  {
                    label: "Day 3",
                    backgroundColor: 'red',
                    data: displayData[2]
                  },
              ]
            };
            chart.data = newData;
            chart.update();
        }

        async function getApiData() {
            const apiResult = await fetch("http://127.0.0.1:8000/covid-cases-predict/");
            const json = await apiResult.json();
            return json;
        }

    }
)();

