// script.js
document.addEventListener('DOMContentLoaded', function() {
    const capacityDiv = document.getElementById('current_spots');
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('Websocket connected!');
    });

    socket.on('spots_update', function(data) {
        capacityDiv.innerText = `Current Capacity: ${data.current_spots}`;
    });
});
