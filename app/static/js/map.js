var map;
var parkingLots = {};

let greenIcon = new L.Icon({
    iconUrl: '/static/images/green-icon.svg',
    iconSize: [25, 41], // size of the icon
    iconAnchor: [12, 41], // point of the icon which will correspond to marker's location
    popupAnchor: [1, -34] // point from which the popup should open relative to the iconAnchor
});

let yellowIcon = new L.Icon({
    iconUrl: '/static/images/yellow-icon.svg',
    iconSize: [25, 41], // size of the icon
    iconAnchor: [12, 41], // point of the icon which will correspond to marker's location
    popupAnchor: [1, -34] // point from which the popup should open relative to the iconAnchor
});

let redIcon = new L.Icon({
    iconUrl: '/static/images/red-icon.svg',
    iconSize: [25, 41], // size of the icon
    iconAnchor: [12, 41], // point of the icon which will correspond to marker's location
    popupAnchor: [1, -34] // point from which the popup should open relative to the iconAnchor
});

async function initMap() {
    let response = await fetch('/api/map_position');
    const { latitude, longitude, zoom } = await response.json()
    map = L.map('mapid').setView([latitude, longitude], zoom); // Set campus coordinates
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    map.setMaxBounds(map.getBounds());
    response = await fetch('/api/parking_lots');
    lots = await response.json();
    for (let id in lots) {
        let lot = lots[id];
        const marker = L.marker([lot.latitude, lot.longitude], {icon: greenIcon}).addTo(map).bindPopup('Loading...');
        parkingLots[id] = marker;
    }
}

function updateParkingLotMarkers(data) {
    for (var lotId in data) {
        var lotData = data[lotId];
        var marker = parkingLots[lotId];
        marker.setPopupContent('Available spots: ' + lotData.available);
        changeMarkerColor(marker, lotData.available, lotData.capacity);
    }
}

function changeMarkerColor(marker, available, capacity) {
    marker.setIcon(getIconForLot(available, capacity));
}

function getIconForLot(available, capacity) {
    const availabilityPercentage = (available / capacity) * 100;

    if (availabilityPercentage > 75) {
        return greenIcon;
    } else if (availabilityPercentage > 25) {
        return yellowIcon;
    } else {
        return redIcon;
    }
}
