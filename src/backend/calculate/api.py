from flask import Flask, jsonify
from flask_cors import CORS
from overpaid_score import get_overpaid_underpaid_data

app = Flask(__name__)
CORS(app)

@app.route('/api/overpaid-players')
def overpaid_players():
    data = get_overpaid_underpaid_data()
    return jsonify(data['overpaid_players'])

@app.route('/api/highest-paid-players')
def highest_paid_players():
    data = get_overpaid_underpaid_data()
    return jsonify(data['highest_paid_players'])

@app.route('/api/underpaid-players')
def underpaid_players():
    data = get_overpaid_underpaid_data()
    return jsonify(data['underpaid_players'])

if __name__ == '__main__':
    app.run()