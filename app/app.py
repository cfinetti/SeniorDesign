from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
from data import parking_lots, map_start_position
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)

def emit_parking():
    socketio.emit('parking_update', parking_lots)

@socketio.on('connect')
def on_connect():
    emit_parking()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/increase/<lot_id>', methods=['POST'])
def increase_available_spots(lot_id):

    if lot_id not in parking_lots:
        return jsonify({'error': 'Invalid parking lot ID'}), 404
              
    parking_lots[lot_id]['available'] += 1
    if parking_lots[lot_id]['available'] <= parking_lots[lot_id]['capacity']:
        emit_parking()

    return jsonify({'success': True, 'lot_id': 'lot_id'}), 200

@app.route('/decrease/<lot_id>', methods=['POST'])
def decrease_available_spots(lot_id):

    if lot_id not in parking_lots:
        return jsonify({'error': 'Invalid parking lot ID'}), 404
    
    parking_lots[lot_id]['available'] -= 1
    if parking_lots[lot_id]['available'] >= 0:
        emit_parking()
    
    return jsonify({'success': True, 'lot_id': 'lot_id'}), 200

@app.route('/api/parking_lots')
def get_parking_lots():
    return jsonify(parking_lots)

@app.route('/api/map_position')
def get_map_position():
    return jsonify(map_start_position)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
