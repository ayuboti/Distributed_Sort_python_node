from flask import Blueprint, request, jsonify, render_template
from .sorting import sort_numbers  # Ensure you have a sorting function defined in sorting.py
from .rabbitmq_config import send_data, receive_data, process_message  # Import RabbitMQ functions
import random

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Render an HTML form for input (the file index.html must be in the templates folder)
    return render_template('index.html')

@main.route('/sort', methods=['POST'])
def sort():
    data = request.form['numbers']
    try:
        # Convert input string to a list of integers
        numbers = list(map(int, data.split(',')))
        # Sort the numbers using the sorting function from sorting.py
        sorted_numbers = sort_numbers(numbers)
        # Send the sorted numbers to RabbitMQ
        send_data(sorted_numbers)
        return jsonify(sorted_numbers)  # Send back the sorted numbers as JSON
    except ValueError:
        # Handle the case where conversion fails
        return jsonify({"error": "Invalid input. Please enter a list of numbers separated by commas."}), 400

@main.route('/generate', methods=['POST'])
def generate():
    data = request.form['total_numbers']
    try:
        # Check if the input is a valid integer
        count = int(data)
        if count > 0:
            numbers = [random.randint(1, 1000) for _ in range(count)]
            # Sort the numbers using the sorting function from sorting.py
            sorted_numbers = sort_numbers(numbers)
            # Send the sorted numbers to RabbitMQ
            send_data(sorted_numbers)
            return jsonify(sorted_numbers)  # Send back the sorted numbers as JSON
        else:
            return jsonify({"error": "Invalid input. Please enter a positive integer."}), 400
    except ValueError:
        # Handle the case where conversion fails
        return jsonify({"error": "Invalid input. Please enter a valid integer."}), 400

@main.route('/receive', methods=['POST'])
def receive():
    receive_data(process_message)  # Example receiving from RabbitMQ
    return jsonify({"message": "Receiving data..."}), 200
