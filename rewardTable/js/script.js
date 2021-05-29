$(document).ready(function () {
    $.getJSON("https://heliumfrontend.s3.amazonaws.com/data.json", function (data) {
        let array = data["Hotspots"];
        let dict = data["Balance"];

        buildBalTable(dict);
        buildTable(array);

        $("th").on("click", function () {
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
        $(document.body).on("click", "td[data-href]", function (){
            $(this).text();
            window.location.href = this.dataset.href
        })

    }).fail(function () {
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
    base_url = "https://mto1ratv44.execute-api.us-east-2.amazonaws.com/default/invoke-HeliumRewards/";
    console.log(base_url)
    for (let i = 0; i < data.length; i++) {
        let row = `<tr>
            <td>${data[i].Hotspot_Owner}</td>
            <td data-href="${base_url}${data[i].Hotspot_Address}">${data[i].Hotspot_Address}</td>
            <td>${data[i].Hotspot_Name}</td>
            <td>${data[i].Hotspot_24H_HNT}</td>
            <td>${data[i].Hotspot_24H_USD}</td>
            <td>${data[i].Change_24H}</td>
            <td>${data[i].Hotspot_30D_HNT}</td>
            <td>${data[i].Hotspot_30D_USD}</td>
            <td>${data[i].Wallet_Balance}</td>
            <td>${data[i].Wallet_Balance_USD}</td>
        </tr>`;
        table.innerHTML += row;
    }
}
