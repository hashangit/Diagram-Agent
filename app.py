from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
import sys
from io import StringIO
from threading import Thread, Event
import queue
import re
import time
import os

# Import your main function and ConsoleInterface
from main import main
from console_interface import ConsoleInterface

app = Flask(__name__, static_folder='templates')
socketio = SocketIO(app, cors_allowed_origins="*")

input_queue = queue.Queue()
input_event = Event()
stop_event = Event()

class WebSocketIOWrapper:
    def __init__(self, console_width=80):
        self.console_interface = ConsoleInterface(width=console_width)
        self.console_width = console_width

    def write(self, message):
        # Convert ANSI color codes to HTML
        html_message = self.ansi_to_html(message)
        socketio.emit('console_output', {'html': html_message, 'text': message})

    def flush(self):
        pass

    def ansi_to_html(self, text):
        ansi_colors = {
            '30': 'black',
            '31': 'red',
            '32': 'green',
            '33': 'yellow',
            '34': 'blue',
            '35': 'magenta',
            '36': 'cyan',
            '37': 'white',
        }

        def replace_color(match):
            code = match.group(1)
            if code in ansi_colors:
                color = ansi_colors[code]
                return f'<span style="color:{color}">'
            elif code == '0':
                return '</span>'
            return ''

        # Replace color codes with HTML spans
        html = re.sub(r'\033\[(\d+)m', replace_color, text)
        # Ensure all spans are closed
        html += '</span>' * html.count('<span')
        return html

    def update_width(self, width):
        self.console_width = width
        self.console_interface.width = width

def custom_input(prompt=''):
    if prompt:
        sys.stdout.write(prompt)
        sys.stdout.flush()
    input_event.set()
    user_input = input_queue.get()
    return user_input

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/styles.css')
def serve_css():
    return send_from_directory(app.static_folder, 'styles.css')

@socketio.on('start_main')
def handle_start_main(data):
    stop_event.clear()
    console_width = data.get('console_width', 80)
    
    def run_main():
        # Add a small delay before starting the main function
        time.sleep(0.5)
        
        old_stdout = sys.stdout
        old_input = __builtins__.input
        sys.stdout = WebSocketIOWrapper(console_width)
        __builtins__.input = custom_input
        try:
            main()
        finally:
            sys.stdout = old_stdout
            __builtins__.input = old_input

    Thread(target=run_main).start()

@socketio.on('stop_current_flow')
def handle_stop_current_flow():
    stop_event.set()
    input_queue.put('STOP')
    input_event.set()

@socketio.on('user_input')
def handle_user_input(data):
    if stop_event.is_set():
        return
    user_input = data['input']
    input_queue.put(user_input)
    socketio.emit('console_output', {'html': user_input + '<br>', 'text': user_input + '\n'})
    input_event.set()

@socketio.on('update_console_width')
def handle_update_console_width(data):
    new_width = data.get('console_width', 80)
    if isinstance(sys.stdout, WebSocketIOWrapper):
        sys.stdout.update_width(new_width)

if __name__ == '__main__':
    socketio.run(app, debug=True)