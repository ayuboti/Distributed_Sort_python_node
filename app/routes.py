from flask import Blueprint, request, jsonify, render_template
from .sorting import sort_numbers  # Ensure you have a sorting function defined in sorting.py
from .communication import send_data, receive_data  # Assuming you have these functions for handling RabbitMQ

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Render an HTML form for input (the file index.html must be in the templates folder)
    return render_template('index.html')

@main.route('/sort', methods=['POST'])
def sort():
    # Get numbers from form input
    data = request.form['numbers']
    try:
        # Convert input string to a list of integers
        numbers = list(map(int, data.split(',')))
        # Sort the numbers using the sorting function from sorting.py
        sorted_numbers = sort_numbers(numbers)
        # You could modify this to send data to another node via RabbitMQ instead
        send_data('sorted_queue', sorted_numbers)  # Example sending to RabbitMQ
        return jsonify(sorted_numbers)  # Send back the sorted numbers as JSON
    except ValueError:
        # Handle the case where conversion fails
        return jsonify({"error": "Invalid input. Please enter a list of numbers separated by commas."}), 400

# Optional: Setup to receive data if necessary for your distributed system
@main.route('/receive', methods=['POST'])
def receive():
    receive_data('sorted_queue', process_message)  # Example receiving from RabbitMQ
    return jsonify({"message": "Receiving data..."}), 200
