import socket
import threading
import tkinter as tk
from tkinter import colorchooser
import json

# Server connection details
SERVER_HOST = '127.0.0.1'  # Change this to the server's IP if on different networks
SERVER_PORT = 12345

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Tkinter setup
root = tk.Tk()
root.title("Real-Time Shared Whiteboard")

# Default drawing settings
current_x, current_y = 0, 0
brush_color = "black"
brush_size = 2

# Canvas setup
canvas = tk.Canvas(root, bg="white", width=800, height=600)
canvas.grid(row=1, column=0, columnspan=5)

# Drawing functions
def on_mouse_press(event):
    global current_x, current_y
    current_x, current_y = event.x, event.y

def on_mouse_move(event):
    global current_x, current_y
    x, y = event.x, event.y
    # Draw line on the canvas
    canvas.create_line(current_x, current_y, x, y, fill=brush_color, width=brush_size)
    # Send drawing data to the server
    data = json.dumps({
        "action": "draw",
        "x1": current_x, "y1": current_y, 
        "x2": x, "y2": y,
        "color": brush_color, 
        "size": brush_size
    })
    client_socket.sendall(data.encode('utf-8'))
    current_x, current_y = x, y

def listen_for_updates():
    """Listen for updates from the server and draw them on the canvas."""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            data = json.loads(message.decode('utf-8'))
            if data["action"] == "draw":
                canvas.create_line(
                    data["x1"], data["y1"], data["x2"], data["y2"],
                    fill=data["color"], width=data["size"]
                )
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# UI Elements for color and brush size
def change_color():
    global brush_color
    color = colorchooser.askcolor()[1]
    if color:
        brush_color = color

def change_brush_size(size):
    global brush_size
    brush_size = size

def clear_canvas():
    # Clear the local canvas and notify the server
    canvas.delete("all")
    data = json.dumps({"action": "clear"})
    client_socket.sendall(data.encode('utf-8'))

# Listen for clear actions from other users
def handle_clear(data):
    canvas.delete("all")

# Add buttons and options
color_button = tk.Button(root, text="Color", command=change_color)
color_button.grid(row=0, column=0)

clear_button = tk.Button(root, text="Clear", command=clear_canvas)
clear_button.grid(row=0, column=1)

brush_size_label = tk.Label(root, text="Brush Size:")
brush_size_label.grid(row=0, column=2)

brush_size_small = tk.Button(root, text="Small", command=lambda: change_brush_size(2))
brush_size_small.grid(row=0, column=3)

brush_size_medium = tk.Button(root, text="Medium", command=lambda: change_brush_size(5))
brush_size_medium.grid(row=0, column=4)

brush_size_large = tk.Button(root, text="Large", command=lambda: change_brush_size(8))
brush_size_large.grid(row=0, column=5)

# Bind mouse events to canvas
canvas.bind("<ButtonPress-1>", on_mouse_press)
canvas.bind("<B1-Motion>", on_mouse_move)

# Start a thread to listen for server updates
def process_updates():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            data = json.loads(message.decode('utf-8'))
            if data["action"] == "draw":
                canvas.create_line(
                    data["x1"], data["y1"], data["x2"], data["y2"],
                    fill=data["color"], width=data["size"]
                )
            elif data["action"] == "clear":
                handle_clear(data)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

update_thread = threading.Thread(target=process_updates, daemon=True)
update_thread.start()

# Start the Tkinter main loop
root.mainloop()
client_socket.close()
