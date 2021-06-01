$(document).ready(function () {
    
    let hotspotName = "112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg";
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
            console.log(totalArray30day)
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
});


function buildGraph(totalArray, timeArray) {
    const chart = document.getElementById("barChart");
    let lineChart = new Chart(chart, {
        type: "bar",
        data: {
            labels: timeArray,

            datasets: [{
                label: '30 days Reward',
                data: totalArray,
                backgroundColor: 'rgba(240, 128, 128, 0.5)',
                borderColor: 'rgba(240, 128, 128, 1)',
                borderWidth: 2,
                borderRadius: 5,
                borderSkipped: false,
            }]
        },
    })
}

function buildGraph2(totalArray, timeArray) {
    const chart = document.getElementById("barChart2");
    let lineChart = new Chart(chart, {
        type: "bar",
        data: {
            labels: timeArray,

            datasets: [{
                label: '7 days Reward',
                data: totalArray,
                backgroundColor: 'rgba(240, 128, 128, 0.5)',
                borderColor: 'rgba(240, 128, 128, 1)',
                borderWidth: 2,
                borderRadius: 5,
                borderSkipped: false,
            }]
        },
    })
}