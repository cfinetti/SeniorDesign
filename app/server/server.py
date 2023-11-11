from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

def update_spots(spots):
    socketio.emit('spots_update', {'current_spots': spots})
# Defines the starting capacity for the lot.
lot_size = 50
current_spots = lot_size
update_spots(current_spots)
# Route that returns the current capacity



@app.route('/capacity')
def get_capacity():
    return jsonify({'capacity': current_spots})

# Route that returns our homepage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/increase', methods=['POST'])
def increase_capacity():
    global current_spots
    current_spots += 1
    update_spots(current_spots)
    return jsonify({'capacity': current_spots, 'status': 'increased'}), 200

@app.route('/decrease', methods=['POST'])
def decrease_capacity():
    global current_spots
    current_spots -= 1
    update_spots(current_spots)
    return jsonify({'capacity': current_spots, 'status': 'decreased'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
