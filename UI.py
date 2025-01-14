import subprocess
import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import pyautogui
import time

# Function to start the server
def start_server():
    global server_process
    try:
        server_process = subprocess.Popen(
            ["python", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        server_status_label.config(text="Server: Running", fg="green")
        start_server_button.config(state="disabled")
        messagebox.showinfo("Success", "Server started successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start the server: {e}")

# Function to start client instances and arrange them
def start_clients():
    global client_processes
    try:
        # Start two instances of client.py
        client1 = subprocess.Popen(["python", "client_ui.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        client2 = subprocess.Popen(["python", "client_ui.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        client_processes.extend([client1, client2])
        client_status_label.config(text="Clients: Running", fg="green")
        start_clients_button.config(state="disabled")
        messagebox.showinfo("Success", "Two client instances started!")

        # Wait for windows to appear and arrange them
        time.sleep(3)  # Give time for client windows to open
        arrange_clients()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start client instances: {e}")

# Function to arrange client windows in full-screen split-screen
def arrange_clients():
    windows = gw.getWindowsWithTitle("Real-Time Shared Whiteboard")
    if len(windows) >= 2:
        # Get screen dimensions using pyautogui
        screen_width, screen_height = pyautogui.size()

        # Arrange clients to cover the full screen in split-screen
        windows[0].resizeTo(screen_width // 2, screen_height)
        windows[0].moveTo(0, 0)
        windows[1].resizeTo(screen_width // 2, screen_height)
        windows[1].moveTo(screen_width // 2, 0)
    else:
        messagebox.showerror("Error", "Could not find client windows to arrange!")

# Function to stop the server and clients
def stop_all():
    global server_process, client_processes
    # Stop server
    if server_process:
        server_process.terminate()
        server_process = None
        server_status_label.config(text="Server: Stopped", fg="red")
        start_server_button.config(state="normal")
    # Stop clients
    for client_process in client_processes:
        client_process.terminate()
    client_processes = []
    client_status_label.config(text="Clients: Stopped", fg="red")
    start_clients_button.config(state="normal")
    messagebox.showinfo("Success", "Stopped server and clients!")

# UI setup
root = tk.Tk()
root.title("Enhanced Server and Client Launcher")
root.geometry("400x300")
root.configure(bg="#f5f5f5")

# Title label
title_label = tk.Label(root, text="Server and Client Manager", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#333")
title_label.pack(pady=10)

# Status frame
status_frame = tk.Frame(root, bg="#f5f5f5")
status_frame.pack(pady=10)

server_status_label = tk.Label(status_frame, text="Server: Stopped", font=("Arial", 12), bg="#f5f5f5", fg="red")
server_status_label.pack(side="top", pady=5)

client_status_label = tk.Label(status_frame, text="Clients: Stopped", font=("Arial", 12), bg="#f5f5f5", fg="red")
client_status_label.pack(side="top", pady=5)

# Button frame
button_frame = tk.Frame(root, bg="#f5f5f5")
button_frame.pack(pady=20)

start_server_button = tk.Button(button_frame, text="Start Server", command=start_server, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, height=2)
start_server_button.grid(row=0, column=0, padx=10, pady=5)

start_clients_button = tk.Button(button_frame, text="Start Clients", command=start_clients, font=("Arial", 12), bg="#2196F3", fg="white", width=20, height=2)
start_clients_button.grid(row=1, column=0, padx=10, pady=5)

stop_button = tk.Button(button_frame, text="Stop All", command=stop_all, font=("Arial", 12), bg="#f44336", fg="white", width=20, height=2)
stop_button.grid(row=2, column=0, padx=10, pady=5)

# Initialize process variables
server_process = None
client_processes = []

# Ensure all processes are terminated when closing the app
def on_closing():
    stop_all()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
