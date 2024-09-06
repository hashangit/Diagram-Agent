from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import sys
from io import StringIO
from threading import Thread, Event
import queue
import re

# Import your main function and ConsoleInterface
from main import main
from console_interface import ConsoleInterface

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

input_queue = queue.Queue()
input_event = Event()
stop_event = Event()

class WebSocketIOWrapper:
    def __init__(self):
        self.console_interface = ConsoleInterface()

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

@socketio.on('start_main')
def handle_start_main():
    stop_event.clear()
    def run_main():
        old_stdout = sys.stdout
        old_input = __builtins__.input
        sys.stdout = WebSocketIOWrapper()
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

if __name__ == '__main__':
    socketio.run(app, debug=True)