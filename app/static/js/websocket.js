var socket;

function initWebSocket() {
    socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('parking_update', function(data) {
        updateParkingLotMarkers(data);
    });
}

