var socket;

function initWebSocket() {
    socket = io.connect('//' + document.domain + ':' + location.port);
    socket.on('parking_update', function(data) {
        updateParkingLotMarkers(data);
    });
}

