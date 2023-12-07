document.addEventListener('DOMContentLoaded', async function() {
    await initMap();
    initWebSocket();
    socket.emit('client_ready')
});
