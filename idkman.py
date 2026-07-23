import socket
import threading
from queue import Queue

# Target configuration
TARGET = "192.168.1.68"  # Localhost for safe testing
queue = Queue()
open_ports = []

def port_scan(port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # Fast timeout for speed
        # Try to connect to the port
        result = s.connect_ex((TARGET, port))
        if result == 0:
            print(f"[+] Port {port} is OPEN")
            open_ports.append(port)
        s.close()
    except:
        pass

def worker():
    while not queue.empty():
        port = queue.get()
        port_scan(port)
        queue.task_done()

# Fill queue with ports to scan (e.g., 1 to 500)
for port in range(1, 501):
    queue.put(port)

# Start 100 parallel threads for rapid scanning
for _ in range(100):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

queue.join()
print(f"Scan complete. Open ports: {open_ports}")
