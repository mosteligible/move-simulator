var index = 0;
var map = L.map('map');
var startLat = route[index][1],
    startLon = route[index][0],
    latlon;
var myPosMarker = L.marker([startLat, startLon], title='this').addTo(map);;

var refreshes = setInterval(function() {
        displayMap();
        if (index >= route.length) {
            clearInterval(refreshes);
        }
    }, 500);
window.onload = refreshes;

function displayMap() {
    startLat = route[index][1];
    startLon = route[index][0];
    latlon = new L.LatLng(startLat, startLon)

    // setView with start Point
    map.setView([startLat, startLon], 18);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    { maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // Update Marker position with new coordinate
    myPosMarker.setLatLng([startLat, startLon]).update()
    index += 1;
}
