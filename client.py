import socket
import threading
import tkinter as tk
import json

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

root = tk.Tk()
root.title("Real-Time Shared Whiteboard")

canvas = tk.Canvas(root, bg="white", width=600, height=400)
canvas.pack()

current_x, current_y = 0, 0

def on_mouse_press(event):
    global current_x, current_y
    current_x, current_y = event.x, event.y

def on_mouse_move(event):
    global current_x, current_y
    x, y = event.x, event.y
    canvas.create_line(current_x, current_y, x, y, fill="black", width=2)
    data = json.dumps({"action": "draw", "x1": current_x, "y1": current_y, "x2": x, "y2": y})
    client_socket.sendall(data.encode('utf-8'))
    current_x, current_y = x, y

def listen_for_updates():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            data = json.loads(message.decode('utf-8'))
            if data["action"] == "draw":
                canvas.create_line(data["x1"], data["y1"], data["x2"], data["y2"], fill="black", width=2)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

canvas.bind("<ButtonPress-1>", on_mouse_press)
canvas.bind("<B1-Motion>", on_mouse_move)

update_thread = threading.Thread(target=listen_for_updates, daemon=True)
update_thread.start()

root.mainloop()
client_socket.close()
