$(document).ready(function () {
    $.getJSON("../data.json", function (data) {
        let hotspotName = "112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg";
        let array = data["Witnesses"];
        let url30day = 'https://api.helium.io/v1/hotspots/' + hotspotName + '/rewards/sum?min_time=-30%20day&bucket=day'
        let url7day = 'https://api.helium.io/v1/hotspots/' + hotspotName + '/rewards/sum?min_time=-7%20day&bucket=day'
        let totalArray30day = []
        let timeArray30day = []
        let totalArray7day = []
        let timeArray7day = []
        // for 30 days
        axios.get(url30day)
            .then(response => {
                for (let i = response.data.data.length - 1; i >= 0; i--) {
                    var reward = response.data.data[i]['total'];
                    var data = response.data.data[i]['timestamp'];
                    var time = data.split("T")
                    totalArray30day.push(reward)
                    timeArray30day.push(time[0])
                }
            }, error => {
                console.log(error);
            })
        // for 7 days
        axios.get(url7day)
            .then(response => {
                for (let i = response.data.data.length - 1; i >= 0; i--) {
                    var reward = response.data.data[i]['total'];
                    var data = response.data.data[i]['timestamp'];
                    var time = data.split("T")
                    totalArray7day.push(reward)
                    timeArray7day.push(time[0])
                }
            }, error => {
                console.log(error);
            })

        buildGraph2(totalArray7day, timeArray7day)
        buildGraph(totalArray30day, timeArray30day)

        buildTable(array, hotspotName);
    }).fail(function () {
        console.log("An error has occurred.");
    });
});


function buildTable(data, hotspotName) {
    let table = document.getElementById("myTable");

    let row = `<tr>
        <td>${hotspotName}</td>
        <td>${data.Witnesses_1}</td>
        <td>${data.Witnesses_2}</td>
        <td>${data.Witnesses_3}</td>
        <td>${data.Witnesses_4}</td>
        <td>${data.Witnesses_5_and_up}</td>
        <td>${data.Total_Witnesses_from_1_to_4}</td>
        <td>${data.Total_Witnesses}</td>
    </tr>`;
    table.innerHTML += row;

}

function buildGraph(totalArray, timeArray) {
    console.log("inside the func")
    const chart = document.getElementById("barChart");
    let lineChart = new Chart(chart, {
        type: "bar",
        data: {
            labels: timeArray,

            datasets: [{
                label: '30 days Reward',
                data: totalArray,
                backgroundColor: 'rgba(240, 128, 128, 0.2)',
                borderColor: 'rgba(240, 128, 128, 1)',
                borderWidth: 2,
                borderRadius: 5,
                borderSkipped: false,
            }]
        },
    })
}

function buildGraph2(totalArray, timeArray) {
    console.log("inside the func")
    const chart = document.getElementById("barChart2");
    let lineChart = new Chart(chart, {
        type: "bar",
        data: {
            labels: timeArray,

            datasets: [{
                label: '7 days Reward',
                data: totalArray,
                backgroundColor: 'rgba(240, 128, 128, 0.2)',
                borderColor: 'rgba(240, 128, 128, 1)',
                borderWidth: 2,
                borderRadius: 5,
                borderSkipped: false,
            }]
        },
    })
}