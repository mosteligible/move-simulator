var index = 0;
var map = L.map('map');
console.log(`last_position: ${latest_position}`);
var startLat = latest_position[1],
    startLon = latest_position[0],
    latlon, coordinate;
var myPosMarker = L.marker([startLat, startLon], title='this').addTo(map);;

const mapElement = document.getElementById("map");
const serverSentEvent = new EventSource(`/routes/stream/${route_id}`);

serverSentEvent.onmessage = (event) => {
    coordinate = JSON.parse(event.data);
    startLat = coordinate[1];
    startLon = coordinate[0];
    displayMap();
};

function displayMap() {
    latlon = new L.LatLng(startLat, startLon)

    // setView with start Point
    map.setView([startLat, startLon], 15);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    { maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // Update Marker position with new coordinate
    myPosMarker.setLatLng([startLat, startLon]).update()
    index += 1;
}
