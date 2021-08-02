$(document).ready(function() {
    $.getJSON("../data.json", function(data) {
        let array = data["Hotspots"];
        let dict = data["Balance"];

        buildBalTable(dict);
        buildTable(array);

        $("th").on("click", function() {
            var column = $(this).data("column");
            var order = $(this).data("order");

            if (order == "desc") {
                $(this).data("order", "asc");
                array = array.sort((a, b) => (a[column] > b[column] ? 1 : -1));
            } else {
                $(this).data("order", "asc");
                array = array.sort((a, b) => (a[column] < b[column] ? 1 : -1));
            }
            buildTable(array);
        });
        // Adds the even listeners for the hotspots addr
        $(document.body).on("click", "td[data-href]", function() {
            $(this).text();
            window.location.href = this.dataset.href;
        });
    }).fail(function() {
        console.log("An error has occurred.");
    });
});

function buildBalTable(data) {
    let table = document.getElementById("myBalTable");
    let row = `<tr>
        <td>${data.Hotspots_24H_HNT}</td>
        <td>${data.Hotspots_24H_USD}</td>
        <td>${data.Hotspots_30D_HNT}</td>
        <td>${data.Hotspots_30D_USD}</td>
        <td>${data.Total_HNT}</td>
        <td>${data.Total_USD}</td>
     </tr>`;
    table.innerHTML += row;
}

function buildTable(data) {
    let table = document.getElementById("myTable");
    table.innerHTML = "";
    base_url =
        "https://gfz4azqik2.execute-api.us-east-2.amazonaws.com/default/invoke-HeliumRewards/";

    console.log(base_url);
    for (let i = 0; i < data.length; i++) {
        let heliumExplorer_url = "https://explorer.helium.com/hotspots/";
        let syncedColor;
        let changeColor;
        let rewardColor;
        // Color for reward Scale
        if (data[i].Reward_Scale > 0.7) {
            rewardColor = "lightgreen";
        } else if ((data[i].Reward_Scale < 0.7) & (data[i].Reward_Scale >= 0.5)) {
            rewardColor = "yellow";
        } else {
            rewardColor = "red";
        }
        if (data[i].Synced_Status == "Synced") {
            syncedColor = "lightgreen";
        } else {
            syncedColor = "red";
        }
        if (data[i].Change_24H >= 0) {
            changeColor = "lightgreen";
        } else {
            changeColor = "red";
        }

        let row = `<tr>
            <td data-href="${heliumExplorer_url}${data[i].Hotspot_Address}">${data[i].Hotspot_Owner}</td>
            <td data-href="${base_url}${data[i].Hotspot_Address}">${data[i].Hotspot_Name}</td>
            <td>${data[i].Hotspot_24H_HNT}</td>
            <td style="color :${changeColor}">${data[i].Change_24H}</td>
            <td style="color :${syncedColor} ">${data[i].Synced_Status}</td>
            <td>${data[i].Hotspot_30D_HNT}</td>
            <td>${data[i].Wallet_Balance}</td>
        </tr>`;
        table.innerHTML += row;
    }
}