import subprocess

# Define the command you want to run
command = "python client.py"

# Define the path where you want to run the command
path = r"C:\Users\bhara\Documents\CN\TCP"  # Replace with your target path

# Run the command in cmd at the specified path and keep the window open
subprocess.run(["cmd", "/k", command], cwd=path)
