let url30day =
    "https://api.helium.io/v1/hotspots/" +
    hotspotName +
    "/rewards/sum?min_time=-30%20day&bucket=day";
let url1day =
    "https://api.helium.io/v1/hotspots/" +
    hotspotName +
    "/rewards/sum?min_time=-1%20day&bucket=hour";
let name = "https://api.helium.io/v1/hotspots/" + hotspotName;
let totalArray30day = [];
let timeArray30day = [];
let list30Day = [];
let totalArray1day = [];
let timeArray1day = [];
let list1Day = [];

axios.get(name).then(
    (response) => {
        let hName = response.data.data["name"];

        buildTable(array, hName);
    },
    (error) => {
        console.log(error);
    }
);

axios.get(url30day).then(
    (response) => {
        var count = 0;
        for (let i = response.data.data.length - 1; i >= 0; i--) {
            var reward = response.data.data[i]["total"];
            var data = response.data.data[i]["timestamp"];
            var time = data.split("T");
            totalArray30day.push(reward);
            timeArray30day.push(time[0]);
            list30Day.push([timeArray30day[count], totalArray30day[count]]);
            count++;
        }
        buildGraph2(list30Day);
    },
    (error) => {
        console.log(error);
    }
);
// for 7 days
axios.get(url1day).then(
    (response) => {
        var count = 0;
        for (let i = response.data.data.length - 1; i >= 0; i--) {
            var reward = response.data.data[i]["total"];
            var time = response.data.data[i]["timestamp"];
            totalArray1day.push(reward);
            timeArray1day.push(time);
            list1Day.push([timeArray1day[count], totalArray1day[count]]);
            count++;
        }

        buildGraph(list1Day);
    },
    (error) => {
        console.log(error);
    }
);

function buildTable(data, hName) {
    let table = document.getElementById("myTable");
    let row = `<tr>
                <td>${hName}</td>
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

function buildGraph(list7Day) {
    Highcharts.chart("con7day", {
        chart: {
            backgroundColor: "#2C3446",
            type: "column",
        },
        title: {
            text: "24 Hour Reward",
            style: {
                color: "#FB667A",
                font: 'bold 16px "Trebuchet MS", Verdana, sans-serif',
            },
        },

        xAxis: {
            type: "category",
            labels: {
                rotation: -45,
                style: {
                    fontSize: "13px",
                    fontFamily: "Verdana, sans-serif",
                },
            },
        },
        yAxis: {
            min: 0,
            title: {
                text: "HNT",
            },
        },
        legend: {
            enabled: false,
        },
        tooltip: {
            pointFormat: "HNT: <b>{point.y:.1f} HNT</b>",
        },
        series: [{
            name: "HNT",
            data: list7Day,
            color: "#FB667A",
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: "#FFFFFF",
                align: "right",
                format: "{point.y:.1f}", // one decimal
                y: 20, // 10 pixels down from the top
                style: {
                    fontSize: "13px",
                    fontFamily: "Verdana, sans-serif",
                },
            },
        }, ],
    });
}

function buildGraph2(list30Day) {
    Highcharts.chart("con30day", {
        chart: {
            backgroundColor: "#2C3446",
            type: "column",
        },
        title: {
            text: "30 Day Reward",
            style: {
                color: "#FB667A",
                font: 'bold 16px "Trebuchet MS", Verdana, sans-serif',
            },
        },
        xAxis: {
            type: "category",
            labels: {
                rotation: -45,
                style: {
                    fontSize: "13px",
                    fontFamily: "Verdana, sans-serif",
                },
            },
        },
        yAxis: {
            min: 0,
            title: {
                text: "HNT",
            },
        },
        legend: {
            enabled: false,
        },
        tooltip: {
            pointFormat: "HNT: <b>{point.y:.1f} HNT</b>",
        },
        series: [{
            name: "HNT",
            data: list30Day,
            color: "#FB667A",
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: "#2C3446",
                align: "right",
                format: "{point.y:.1f}", // one decimal
                y: 5, // 10 pixels down from the top
                style: {
                    fontSize: "10px",
                    fontFamily: "Verdana, sans-serif",
                },
            },
        }, ],
    });
}