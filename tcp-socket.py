import socket

def start_server():
    HOST = '127.0.0.1'  # localhost
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()  # Listen for connections
        print(f"Server listening on {HOST}:{PORT}")
        
        conn, addr = server.accept()  # Accept a client
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)  # Receive up to 1024 bytes
                if not data:
                    break
                conn.sendall(data)  # Echo back

if __name__ == "__main__":
    start_server()