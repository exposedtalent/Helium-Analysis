from botocore.exceptions import ClientError
import boto3


def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("HotspotRewards")    
    response = table.scan()
    hotspotRewards = response['Items']
    table2 = dynamodb.Table("HeliumRewardsDict")
    response = table2.scan()
    HotspotRewardsDict = response['Items']
    
    # Dynamically adding data from the varibles into a string used for js script
    balanceHtmlDict = """let dict = %s"""%HotspotRewardsDict
    # Dynamically adding data from the varibles into a string used for js script
    hotspotsHtmlList = """\nlet array = %s"""%hotspotRewards

    # Top half of the html with inline css code. This creates a table and style it using css
    topHtml = """
    <!DOCTYPE html><html ><head>
      <meta charset="UTF-8">
      <title>Wifi Mist</title>
          <script src="https://code.jquery.com/jquery-1.11.0.min.js"></script>

      <script src="https://s.codepen.io/assets/libs/modernizr.js" type="text/javascript"></scrip>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
  <link rel="stylesheet" href="https://heliumfrontend.s3.amazonaws.com/newStyle.css">

    </head>
<body>
<!-- partial:index.partial.html -->
<h1><span class="peach">Balance</pan></h1>
<table class="container">
	<thead>
		<tr>
			<th> HNT Price</th>
			<th> 24H HNT</th>
			<th> 24H USD</th>
			<th > 30D HNT</th>
			<th> 30D USD</th>
			<th > HNT</th>
			<th > USD</th>

  			<tbody id="myBalTable">
		</tr>
	</thead>
</table>
<h1><span class="peach">Hotspot Information</pan></h1>
<table class="container">
	<thead>
		<tr>
			<th data-column='HotspotOwner' data-order='desc'> Owner &#9650</th>
			<th data-column='HotspotName' data-order='desc'> Name &#9650</th>
			<th data-column='Hotspot24HHNT' data-order='desc'> Status &#9650</th>
			<th data-column='Change' data-order='desc'>24H HNT  &#9650</th>
			<th data-column='Synced Status' data-order='desc'>Change &#9650</th>
			<th data-column='Hotspot30DHNT' data-order='desc'> 30D HNT &#9650</th>
			<th data-column='WalletBalance' data-order='desc'> Balance &#9650</th>
			</tr>
			<tbody id="myTable">
		</tr>
	</thead>
</table>
<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
        <script>
    """
    # This is the bottom of the html with js script inline
    bottomHtml = """
    $('th').on('click', function(){
                var column = $(this).data('column')
                var order = $(this).data('order')

                if(order == 'desc'){
                    $(this).data('order', "asc")
                    array = array.sort((a,b) => a[column] > b[column]? 1 : -1)   
                }
                else{
                    $(this).data('order', "asc")
                    array = array.sort((a,b) => a[column] < b[column]? 1 : -1)
                }
                buildTable(array)
            
            })
     $(document.body).on("click", "td[data-href]", function (){
            $(this).text();
            window.location.href = this.dataset.href
        })
    buildTable(array)
    buildBalTable(dict)
    
    
    function buildBalTable(data){
        let table = document.getElementById("myBalTable")
        let row = `<tr>
            <td>${data[0].HNT_Price}</td>
            <td>${data[0].Hotspots_24H_HNT}</td>
            <td>${data[0].Hotspots_24H_USD}</td>
            <td>${data[0].Hotspots_30D_HNT}</td>
            <td>${data[0].Hotspots_30D_USD}</td>
            <td>${data[0].Total_HNT}</td>
            <td>${data[0].Total_USD}</td>
         </tr>`
        table.innerHTML += row
    
    }
    
    function buildTable(data) {
    let table = document.getElementById("myTable");
    table.innerHTML = "";
    base_url = "https://gfz4azqik2.execute-api.us-east-2.amazonaws.com/default/invoke-HeliumRewards/";
    for (let i = 0; i < data.length; i++) {
        let syncedColor;
        let changeColor;
        if (data[i].Synced_Status == "Synced") {
            syncedColor = 'lightgreen';
        } else {
            syncedColor = 'red';
        }
        if (data[i].Change_24H >= 0) {
            changeColor = 'lightgreen';
        } else {
            changeColor = 'red';
        }

        let row = `<tr>
            <td>${data[i].Hotspot_Owner}</td>
            <td data-href="${base_url}${data[i].Hotspot_Address}">${data[i].Hotspot_Name}</td>
            <td style="color :${syncedColor} ">${data[i].Synced_Status}</td>
            <td>${data[i].Hotspot_24H_HNT}</td>
            <td style="color :${changeColor}">${data[i].Change_24H + "%"}</td>
            <td>${data[i].Hotspot_30D_HNT}</td>
            <td>${data[i].Wallet_Balance}</td>
        </tr>`;
        table.innerHTML += row;
        }
    }
      </script>
    
    
    </body>
    </html>
    """
    # Finally put together the differernt html strings into one to be returned
    finalHtml = topHtml + balanceHtmlDict + hotspotsHtmlList + bottomHtml

    # returns the final html string and that is run on the client side
    return{
        # "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": finalHtml
    }



