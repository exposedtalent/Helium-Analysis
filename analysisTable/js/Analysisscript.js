$(document).ready(function () {
    $.getJSON("../data.json", function (data) {
        let hotspotName = "112XTwrpTBHjg4M1DWsLTcqsfJVZCPCYW2vNPJV7cZkpRg3JiKEg";
        let array = data["Witnesses"];
        buildTable(array, hotspotName);
    }).fail(function () {
        console.log("An error has occurred.");
    });
});


function buildTable(data, hotspotName) {
    console.log(data);
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
