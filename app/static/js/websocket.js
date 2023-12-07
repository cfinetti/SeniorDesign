function initWebSocket() {
    socket.on('parking_update', function(data) {
        updateParkingLotMarkers(data);
    });
}

