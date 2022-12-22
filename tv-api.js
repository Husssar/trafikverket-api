
var xmlRequest = "<REQUEST>" +
    // Use your valid authenticationkey
    "<LOGIN authenticationkey='put-key-here'/>" +

    "<QUERY objecttype='WeatherStation' schemaversion='1'>" +
    "<FILTER>" +
    "<AND>" +
    "<EQ name='CountyNo' value='13' />" +
    "<OR>" +
    "<EQ name='Name' value='Vrangelsro' />" +
    "</OR></AND>" +
    "</FILTER>" +
    "<INCLUDE>Active</INCLUDE>" +
    "<INCLUDE>CountyNo</INCLUDE>" +
    "<INCLUDE>Geometry.SWEREF99TM</INCLUDE>" +
    "<INCLUDE>Measurement</INCLUDE>" +
    "<INCLUDE>Name</INCLUDE>"+
    "<INCLUDE>RoadNumberNumeric</INCLUDE>"+

    "</QUERY>" +
    "</REQUEST>";

(async () => {
    const rawResponse = await fetch('https://api.trafikinfo.trafikverket.se/v2/data.json', {


        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'text/xml'
        },
        body: xmlRequest
    });
    const content = await rawResponse.json();

    console.log(content.RESPONSE.RESULT[0].WeatherStation[0])

})();
