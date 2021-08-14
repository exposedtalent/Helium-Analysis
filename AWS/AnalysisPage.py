from datetime import date, timedelta
import boto3
from boto3.dynamodb.conditions import Key,Attr
from decimal import Decimal

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("HotspotWitnesses")
    table2 = dynamodb.Table("HotspotBeacons")
    
    todayDate = date.today()
    today = '%s'%todayDate
    td = timedelta(1)
    d = todayDate + td
    upperDate = '%s'%d
    d = todayDate - td
    lowerDate = '%s'%d
    
    # gets the uri from the url
    hotspots = []
    path = event['path']
    x = path.split("/")
    hotspots.append(x[2])
    

    response = table2.query(
    #   FilterExpression= Attr("Witnesses").between(1,5),
       KeyConditionExpression=Key('Hotspot').eq(hotspots[0]) & Key('BeaconTime').between(lowerDate, upperDate)
    )
    beaconLen = len(response['Items'])
    
    occurOne = occurTwo = occurThree = occurFour = occurMore = 0
    
    data = table.query(
        FilterExpression = Attr("Witnesses").eq(1),
        KeyConditionExpression = Key("Hotspot").eq(hotspots[0]) & Key("WitnesseTime").between(lowerDate, upperDate)
    )
    occurOne = len(data['Items'])
    
    data = table.query(
        FilterExpression = Attr("Witnesses").eq(2),
        KeyConditionExpression = Key("Hotspot").eq(hotspots[0]) & Key("WitnesseTime").between(lowerDate, upperDate)
    )
    occurTwo = len(data['Items'])

    data = table.query(
        FilterExpression = Attr("Witnesses").eq(3),
        KeyConditionExpression = Key("Hotspot").eq(hotspots[0]) & Key("WitnesseTime").between(lowerDate, upperDate)
    )
    occurThree = len(data['Items'])

    data = table.query(
        FilterExpression = Attr("Witnesses").eq(4),
        KeyConditionExpression = Key("Hotspot").eq(hotspots[0]) & Key("WitnesseTime").between(lowerDate, upperDate)
    )
    occurFour = len(data['Items'])

    data = table.query(
        FilterExpression = Attr("Witnesses").between(5, 25),
        KeyConditionExpression = Key("Hotspot").eq(hotspots[0]) & Key("WitnesseTime").between(lowerDate, upperDate)
    )

    occurMore = len(data['Items'])
    
    onetofour = occurOne +occurTwo + occurThree + occurFour
    witnesseDict = {
        "Witnesses_1" : occurOne,
        "Witnesses_2" : occurTwo,
        "Witnesses_3" : occurThree,
        "Witnesses_4" : occurFour,
        "Witnesses_5_and_up" : occurMore,
        "Total_Witnesses_from_1_to_4" : onetofour, 
        "Total_Witnesses" : onetofour + occurMore,
        "Beacon": beaconLen

    }
    beacon = []
    for i in range(len(response['Items'])):
        data = {
            'Challengee': response['Items'][i]['Challengee'],
            'Hotspot': response['Items'][i]['Hotspot'],
            'BeaconTime': response['Items'][i]['BeaconTime'],
            'Witnesses': str(response['Items'][i]['Witnesses']),
        }
        beacon.append(data)
    beaconDict = {"beacon": beacon}
    WitnesseshtmlList = """let array = %s;"""%witnesseDict
    hotspotName = """\nlet hotspotName = "%s";"""%hotspots[0]
    beaconhtml = """\nlet beacon = %s;"""%beacon
    htmlTop = """
        <!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>WifiMist</title>
  <link rel="stylesheet" href="https://heliumfrontend.s3.amazonaws.com/newStyle.css">
  <script src="https://code.highcharts.com/highcharts.js"></script>
  <script src="https://code.highcharts.com/modules/exporting.js"></script>
  <script src="https://code.highcharts.com/modules/export-data.js"></script>
  <script src="https://code.highcharts.com/modules/accessibility.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.min.js"></script>
  <link rel="shortcut icon" type="image/jpg" href="https://heliumfrontend.s3.amazonaws.com/LogoWifimist.jpg"/>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.21.1/axios.js" integrity="sha512-otOZr2EcknK9a5aa3BbMR9XOjYKtxxscwyRHN6zmdXuRfJ5uApkHB7cz1laWk2g8RKLzV9qv/fl3RPwfCuoxHQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

</head>
<body>
<h1><span class="peach">Witness Count</pan></h1>
<table class="container">
	<thead>
		<tr>
			<th>  Hotspot </th>
			<th>1 Wit</th>
			<th>2 Wit</th>
			<th >3 Wit</th>
			<th >4 Wit</th>
			<th >5 and up</th>
			<th >Wit 1-4</th>
			<th >Total</th>
			<th >Beacon</th>
  		</tr>
  <tbody id="myTable">
	</thead>
</table>
<h1><span class="peach">Beacons</pan></h1>
<table class="container">
	<thead>
		<tr>
			<th>Time</th>
      <th> Witnesses</th>
  		</tr>
  <tbody id="myTableBeacon">
	</thead>
</table>
</div>
        <script src="https://code.jquery.com/jquery-1.11.0.min.js"></script>
        <h1><span class="peach">24 Hrs & 30 Day Rewards</pan></h1>

        <figure class="highcharts-figure">
          <div id="con7day" ></div>
          </figure>
          <figure class="highcharts-figure">
          <div id="con30day" ></div>
          
        </figure>
        <script>
    """
    htmlBottom = """
        let url30day = 'https://api.helium.io/v1/hotspots/' + hotspotName + '/rewards/sum?min_time=-30%20day&bucket=day'
        let url1day = 'https://api.helium.io/v1/hotspots/' + hotspotName + '/rewards/sum?min_time=-1%20day&bucket=hour'
        let name = 'https://api.helium.io/v1/hotspots/' + hotspotName
        let totalArray30day = []
        let timeArray30day = []
        let list30Day = []
        let totalArray1day = []
        let timeArray1day = []
        let list1Day = []

        axios.get(name)
            .then(response => {
                let hName = response.data.data['name'];
                
                buildTable(array, hName);
            }, error => {
                console.log(error);
            })
        buildBeaconTable(beacon);

        
        axios.get(url30day)
            .then(response => {
                var count = 0;
                for (let i = response.data.data.length - 1; i >= 0; i--) {
                    var reward = response.data.data[i]['total'];
                    var data = response.data.data[i]['timestamp'];
                    var time = data.split("T")
                    totalArray30day.push(reward)
                    timeArray30day.push(time[0])
                    list30Day.push([timeArray30day[count],totalArray30day[count]])
                    count++;
                }
                buildGraph2(list30Day)
                
            }, error => {
                console.log(error);
            })
        // for 24 hrs
        axios.get(url1day)
            .then(response => {
                var count = 0;
                for (let i = response.data.data.length - 1; i >= 0; i--) {
                    var reward = response.data.data[i]['total'];
                    var str = response.data.data[i]['timestamp'];
                    var res = str.split(/(?:T|Z)+/);
                    var temp = res[1];
                    res = temp.split(".");
                    time = res[0];
                    totalArray1day.push(reward)
                    timeArray1day.push(time)
                    list1Day.push([timeArray1day[count], totalArray1day[count]])
                    count++;
                }
                
                buildGraph(list1Day)
            }, error => {
                console.log(error);
            })
        
        
        
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
                <td>${data.Beacon}</td>
            </tr>`;
            table.innerHTML += row;
    
        }
        function buildBeaconTable(data) {
            if(data.length != 0){
                let table = document.getElementById("myTableBeacon");
                table.innerHTML = " ";
                console.log(data.length);
            
                for (let i = 0; i < data.length; i++) {
                    let str = data[i].BeaconTime;
                    let row = `<tr>
                    <td>${str}</td>
                    <td>${data[i].Witnesses}</td>
                    </tr>`;
                    table.innerHTML += row;
                }
            }
            else{
                let table = document.getElementById("myTableBeacon");
                table.innerHTML = " ";

                
                let row = `<tr>
                <td>${null}</td>
                <td>${null}</td>
                </tr>`;
                table.innerHTML += row;
                
            }
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
        plotOptions: {
            series: {
                borderColor: "#FB667A",
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
        plotOptions: {
            series: {
                borderColor: "#FB667A",
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
        </script>
        </body>
        </html>
    """
    
    finalhtml = htmlTop + WitnesseshtmlList + hotspotName +beaconhtml + htmlBottom
    return{
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": finalhtml
    }
    
