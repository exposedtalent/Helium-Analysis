import boto3
from datetime import date, timedelta
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("HotspotRewards")    
    response = table.scan()
    hotspotRewards = response['Items']
    
    
    # todayDate = date.today()
    # today = '%s'%todayDate
    # td = timedelta(1)
    # d = todayDate + td
    # upperDate = '%s'%d
    
    
    
    # response = table3.query(
    # #   FilterExpression= Attr("Witnesses").between(1,5),
    #   KeyConditionExpression=Key('Hotspot').eq(hotspots[0]) & Key('BeaconTime').between(today, upperDate)
    # )
    beaconLen = len(response['Items'])
    # adding data from the varibles into a string used for js script
    hotspotsHtmlList = """\nlet array = %s"""%hotspotRewards
    # adding data from the varibles into a string used for js script
    # beaconHtml = """\nlet beaconList = %s"""%beaconLen 
    # Top half of the html with inline css code. This creates a table and style it using css
    fHtml = """
    
    <!DOCTYPE html>
<html lang="en">
  <script src="https://code.jquery.com/jquery-1.11.0.min.js"></script>

      <script src="https://s.codepen.io/assets/libs/modernizr.js" type="text/javascript"></scrip>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
  <link rel="stylesheet" href="https://heliumfrontend.s3.amazonaws.com/Style1.css">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.21.1/axios.js" integrity="sha512-otOZr2EcknK9a5aa3BbMR9XOjYKtxxscwyRHN6zmdXuRfJ5uApkHB7cz1laWk2g8RKLzV9qv/fl3RPwfCuoxHQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

  <link rel="shortcut icon" type="image/jpg" href="https://heliumfrontend.s3.amazonaws.com/LogoWifimist.jpg"/>
  <body>
    
    <script
      language="JavaScript"
      type="text/javascript"
      src="https://kjur.github.io/jsrsasign/jsrsasign-latest-all-min.js"
    </script>
    <script >
        var key_id;
        var keys;
        var key_index;
        
        //verify token
        async function verifyToken(token) {
            //get Cognito keys
            keys_url =
                "https://cognito-idp." +
                region +
                ".amazonaws.com/" +
                userPoolId +
                "/.well-known/jwks.json";
            await fetch(keys_url)
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    keys = data["keys"];
                });
        
            //Get the kid (key id)
            var tokenHeader = parseJWTHeader(token);
            key_id = tokenHeader.kid;
        
            //search for the kid key id in the Cognito Keys
            const key = keys.find((key) => key.kid === key_id);
            if (key === undefined) {
                return "Public key not found in Cognito jwks.json";
            }
        
            //verify JWT Signature
            var keyObj = KEYUTIL.getKey(key);
            var isValid = KJUR.jws.JWS.verifyJWT(token, keyObj, { alg: ["RS256"] });
            if (isValid) {} else {
                return "Signature verification failed";
            }
        
            //verify token has not expired
            var tokenPayload = parseJWTPayload(token);
            if (Date.now() >= tokenPayload.exp * 1000) {
                return "Token expired";
            }
        
            //verify app_client_id
            var n = tokenPayload.aud.localeCompare(appClientId);
            if (n != 0) {
                return "Token was not issued for this audience";
            }
            return "verified";
        }
    </script>
    <script >
        var myHeaders = new Headers();
        myHeaders.set('Cache-Control', 'no-store');
        var urlParams = new URLSearchParams(window.location.search);
        var tokens;
        var domain = "wifimist";
        var region = "us-east-1";
        var appClientId = "1dbo3ktcigjv6sth9i8oogqv87";
        var userPoolId = "us-east-1_QX7bs20cL";
        var redirectURI = "https://dashboard.wifimist.com/Hotspots";
        
        //Convert Payload from Base64-URL to JSON
        const decodePayload = payload => {
            const cleanedPayload = payload.replace(/-/g, '+').replace(/_/g, '/');
            const decodedPayload = atob(cleanedPayload)
            const uriEncodedPayload = Array.from(decodedPayload).reduce((acc, char) => {
                const uriEncodedChar = ('00' + char.charCodeAt(0).toString(16)).slice(-2)
                return `${acc}%${uriEncodedChar}`
            }, '')
            const jsonPayload = decodeURIComponent(uriEncodedPayload);
        
            return JSON.parse(jsonPayload)
        }
        
        //Parse JWT Payload
        const parseJWTPayload = token => {
            const [header, payload, signature] = token.split('.');
            const jsonPayload = decodePayload(payload)
        
            return jsonPayload
        };
        
        //Parse JWT Header
        const parseJWTHeader = token => {
            const [header, payload, signature] = token.split('.');
            const jsonHeader = decodePayload(header)
        
            return jsonHeader
        };
        
        //Generate a Random String
        const getRandomString = () => {
            const randomItems = new Uint32Array(28);
            crypto.getRandomValues(randomItems);
            const binaryStringItems = randomItems.map(dec => `0${dec.toString(16).substr(-2)}`)
            return binaryStringItems.reduce((acc, item) => `${acc}${item}`, '');
        }
        
        //Encrypt a String with SHA256
        const encryptStringWithSHA256 = async str => {
            const PROTOCOL = 'SHA-256'
            const textEncoder = new TextEncoder();
            const encodedData = textEncoder.encode(str);
            return crypto.subtle.digest(PROTOCOL, encodedData);
        }
        
        //Convert Hash to Base64-URL
        const hashToBase64url = arrayBuffer => {
            const items = new Uint8Array(arrayBuffer)
            const stringifiedArrayHash = items.reduce((acc, i) => `${acc}${String.fromCharCode(i)}`, '')
            const decodedHash = btoa(stringifiedArrayHash)
        
            const base64URL = decodedHash.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
            return base64URL
        }
        
        // Main Function
        async function main() {
            var code = urlParams.get('code');
        
            //If code not present then request code else request tokens
            if (code == null) {
        
                // Create random "state"
                var state = getRandomString();
                sessionStorage.setItem("pkce_state", state);
        
                // Create PKCE code verifier
                var code_verifier = getRandomString();
                sessionStorage.setItem("code_verifier", code_verifier);
        
                // Create code challenge
                var arrayHash = await encryptStringWithSHA256(code_verifier);
                var code_challenge = hashToBase64url(arrayHash);
                sessionStorage.setItem("code_challenge", code_challenge)
        
                // Redirtect user-agent to /authorize endpoint
                location.href = "https://" + domain + ".auth." + region + ".amazoncognito.com/oauth2/authorize?response_type=code&state=" + state + "&client_id=" + appClientId + "&redirect_uri=" + redirectURI + "&scope=openid&code_challenge_method=S256&code_challenge=" + code_challenge;
            } else {
        
                // Verify state matches
                state = urlParams.get('state');
                if (sessionStorage.getItem("pkce_state") != state) {
                    
                } else {
        
                    // Fetch OAuth2 tokens from Cognito
                    code_verifier = sessionStorage.getItem('code_verifier');
                    await fetch("https://" + domain + ".auth." + region + ".amazoncognito.com/oauth2/token?grant_type=authorization_code&client_id=" + appClientId + "&code_verifier=" + code_verifier + "&redirect_uri=" + redirectURI + "&code=" + code, {
                            method: 'post',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            }
                        })
                        .then((response) => {
                            return response.json();
                        })
                        .then((data) => {
        
                            // Verify id_token
                            tokens = data;
                            var idVerified = verifyToken(tokens.id_token);
                            Promise.resolve(idVerified).then(function(value) {
                                if (value.localeCompare("verified")) {
                                    alert("Invalid ID Token - " + value);
                                    return;
                                }
                            });
                            // Display tokens
                            document.getElementById("id_token").innerHTML = JSON.stringify(parseJWTPayload(tokens.id_token), null, '\t');
                            document.getElementById("access_token").innerHTML = JSON.stringify(parseJWTPayload(tokens.access_token), null, '\t');
                        });
        
                    // Fetch from /user_info
                    await fetch("https://" + domain + ".auth." + region + ".amazoncognito.com/oauth2/userInfo", {
                            method: 'post',
                            headers: {
                                'authorization': 'Bearer ' + tokens.access_token
                            }
                        })
                        .then((response) => {
                            return response.json();
                        })
                        .then((data) => {
                            // Display user information
                            document.getElementById("userInfo").innerHTML = JSON.stringify(data, null, '\t');
                        });
                }
            }
        }
        main();
    </script>
  </body>
</html>
"""
    topHtml = """
    <!DOCTYPE html><html ><head>
      <meta charset="UTF-8">
      <title>Wifi Mist</title>
      <link rel="shortcut icon" type="image/jpg" href="https://heliumfrontend.s3.amazonaws.com/LogoWifimist.jpg"/>

          

    </head>
<body>
<h1><span class="peach">Ashok</pan></h1>
<table class="container">
	<thead>
		<tr>
			<th> HNT Price</th>
			<th> 24H HNT</th>
			<th> 24H AVG</th>
			<th> 24H USD</th>
			<th > 30D HNT</th>
			<th> 30D USD</th>
			<th > HNT</th>
			<th > USD</th>

  			<tbody id="AshokTable">
		</tr>
	</thead>
</table>

<h1><span class="peach">Mukesh</pan></h1>
<table class="container">
	<thead>
		<tr>
			<th> HNT Price</th>
			<th> 24H HNT</th>
			<th> 24H AVG</th>
			<th> 24H USD</th>
			<th > 30D HNT</th>
			<th> 30D USD</th>
			<th > HNT</th>
			<th > USD</th>

  			<tbody id="MukeshTable">
		</tr>
	</thead>
</table>



<style>
.buttons {
    display: flex;
    justify-content: flex-end;
    margin-right: 4.5em;
    align-items: center;
}
</style>
<h1><span class="peach">Hotspot Information</pan></h1>
<div class = "buttons">
<button onclick="window.location.href=' https://wxpoj5dnuc.execute-api.us-east-1.amazonaws.com/default/putRewards';">Refresh
</button>
</div>
<table class="container">
	<thead>
		<tr>
			<th data-column='HotspotOwner' data-order='desc'>Owner</th>
			<th data-column='HotspotName' data-order='desc'>Name</th>
			<th data-column='Status' data-order='desc'>Status</th>
			<th data-column='RewardScale' data-order='desc'>Scale</th>
			<th data-column='24HNT' data-order='desc'>24H</th>
			<th data-column='24hchange' data-order='desc'>Change</th>
			<th data-column='Hotspot30DHNT' data-order='desc'>30D</th>
			<th data-column='WalletBalance' data-order='desc'>Balance</th>
			<th data-column='WalletBalance' data-order='desc'>Beacons</th>
			</tr>
			<tbody id="myTable">
		</tr>
	</thead>
</table>
        <script>
    """
    # This is the bottom of the html with js script inline
    bottomHtml = """
    let sync = [];
    let num = array.length - 3;
    let hotspot = [];
    for (let i = 0; i < array.length; i++) {
            hotspot.push(array[i]["Hotspot_Address"]);
            let url = "https://api.helium.io/v1/hotspots/" + hotspot[i];
            axios.get(url).then(
                (response) => {
                    sync.push(response["data"]["data"]["status"]["online"]);
                },
                (error) => {
                    console.log(error);
                }
            );
        }
    
    array.sort(function(a, b) {
            return b.Hotspot_24H_HNT - a.Hotspot_24H_HNT;
        });
    buildTable(array)
     $(document.body).on("click", "td[data-href]", function (){
            $(this).text();
            window.location.href = this.dataset.href
        })
    let AshTable = []
    let MukeshTable = []
    let NormalTable = []
    for (let i = 0; i < array.length; i++) {
    
        if (array[i]['Hotspot_Owner'].match(/Ash/g)) {
            AshTable.push(array[i]);
        }
       
        else if(array[i]['Hotspot_Owner'].match(/Mukesh/g)){
            MukeshTable.push(array[i]);
        }
        
    }
    let hntAPI = 'https://api.binance.com/api/v3/ticker/price?symbol=HNTUSDT'
    let HNTPrice;
    
    axios.get(hntAPI).then(
        (response) => {
            console.log(response)
            HNTPrice = response['data']['price']
            console.log(HNTPrice)
            buildBalTableAsh(AshTable, HNTPrice)
            buildBalTableMukesh(MukeshTable, HNTPrice)

        },
        (error) => {
            console.log(error);
        }
    );
    
    
    function buildBalTableAsh(data, price) {
    let hotspot24hrs = [];
    let hotspot24AVG;
    let hotspot30day = [];
    let total = [];

    for (let i = 0; i < data.length; i++) {
        hotspot24hrs.push(Number(data[i]['Hotspot_24H_HNT']));
        hotspot30day.push(Number(data[i]['Hotspot_30D_HNT']));
        total.push(Number(data[i]['Wallet_Balance']));
    }
    const sum24hrs = hotspot24hrs.reduce((a, b) => a + b)
    hotspot24AVG = sum24hrs / data.length;
    const sum30day = hotspot30day.reduce((a, b) => a + b)
    const totalBal = total.reduce((a,b) => a + b)
    
    let table = document.getElementById("AshokTable");
        let row = `<tr>
            <td>${Math.round(price * 100) / 100 }</td>
            <td>${Math.round(sum24hrs * 100 ) /100}</td>
            <td>${Math.round(hotspot24AVG * 100) / 100}</td>
            <td>${Math.round((sum24hrs * price) * 100)/ 100}</td>
            <td>${Math.round(sum30day * 100) / 100}</td>
            <td>${Math.round((sum30day * price) * 100 ) /100}</td>
            <td>${Math.round(totalBal * 100) / 100}</td>
            <td>${Math.round((totalBal * price) * 100) / 100}</td>
            </tr>`;
        table.innerHTML += row;
    
}
    function buildBalTableMukesh(data, price) {
        let hotspot24hrs = [];
        let hotspot24AVG;
        let hotspot30day = [];
        let total = [];
    
        for (let i = 0; i < data.length; i++) {
            hotspot24hrs.push(Number(data[i]['Hotspot_24H_HNT']));
            hotspot30day.push(Number(data[i]['Hotspot_30D_HNT']));
            total.push(Number(data[i]['Wallet_Balance']));
        }
        const sum24hrs = hotspot24hrs.reduce((a, b) => a + b)
        hotspot24AVG = sum24hrs / data.length;
        const sum30day = hotspot30day.reduce((a, b) => a + b)
        const totalBal = total.reduce((a,b) => a + b)
        
        let table = document.getElementById("MukeshTable");
            let row = `<tr>
            <td>${Math.round(price * 100) / 100 }</td>
            <td>${Math.round(sum24hrs * 100 ) /100}</td>
            <td>${Math.round(hotspot24AVG * 100) / 100}</td>
            <td>${Math.round((sum24hrs * price) * 100)/ 100}</td>
            <td>${Math.round(sum30day * 100) / 100}</td>
            <td>${Math.round((sum30day * price) * 100 ) /100}</td>
            <td>${Math.round(totalBal * 100) / 100}</td>
            <td>${Math.round((totalBal * price) * 100) / 100}</td>
            </tr>`;
        table.innerHTML += row;
    
    }

    
    function buildTable(data) {
    let table = document.getElementById("myTable");
    table.innerHTML = "";
    let base_url = "https://dashboard.wifimist.com/Hotspots/";
    let heliumExplorer_url = "https://explorer.helium.com/hotspots/";
    let syncedColor;
    let changeColor;
    let rewardColor;
    
    
        
    for (let i = 0; i < data.length; i++) {
        // Color for Synced
        if (data[i].Synced_Status == "Synced") {
            syncedColor = "&#x1f7e2;";
        } else if (data[i].Synced_Status== "Offline") {
            syncedColor = "&#128308;";
        } else if (data[i].Synced_Status == "Not Synced") {
            syncedColor = "&#128992;";
        }
        // Color for 24 H change
        if (data[i].Change_24H >= 0) {
            changeColor = 'lightgreen';
        } else {
            changeColor = 'red';
        }
        // Color for reward Scale
        if(data[i].Reward_Scale > 0.7){
            rewardColor = 'lightgreen';
        }
        else if (data[i].Reward_Scale < 0.7 & data[i].Reward_Scale >= 0.5 ){
            rewardColor = 'yellow';
        }
        else{
            rewardColor = 'red';
        }
        

        let row = `<tr>
            <td data-href="${heliumExplorer_url}${data[i].Hotspot_Address}">${data[i].Hotspot_Owner}</td>
            <td data-href="${base_url}${data[i].Hotspot_Address}">${data[i].Hotspot_Name}</td>
            <td >${data[i].Block_Difference + " " }${syncedColor}</td>
            <td style="color :${rewardColor}">${data[i].Reward_Scale}</td>
            <td>${data[i].Hotspot_24H_HNT}</td>
            <td style="color :${changeColor}">${data[i].Change_24H + "%"}</td>
            <td>${data[i].Hotspot_30D_HNT}</td>
            <td>${data[i].Wallet_Balance}</td>
            <td>${data[i].Beacon}</td>
        </tr>`;
        table.innerHTML += row;
        }
    }
      </script>
    
    
    </body>
    </html>
    """
    # Finally put together the different html strings into one to be returned
    finalHtml =  fHtml + topHtml + hotspotsHtmlList  + bottomHtml
    
    # returns the final html string and that is run on the client side
    return{
        # "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": finalHtml
    }



