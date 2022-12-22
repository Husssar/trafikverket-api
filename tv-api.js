
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

//const rawResponse = await fetch('https://webhook.site/0980d70f-97c7-4391-80ec-5ebf9d95f8cd', {
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
    //   console.log(content.RESPONSE.RESULT[0].WeatherStation.Active)
    //console.log(content.RESPONSE.RESULT[0].WeatherStation[0].Active)

    console.log(content.RESPONSE.RESULT[0].WeatherStation[0])

    // console.log(content.RESPONSE.RESULT[0].WeatherStation[0].Measurement)

})();
