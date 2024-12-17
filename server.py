import socket
from cryptography.fernet import Fernet

# Generate a symmetric key
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Server binds to localhost on port 12345
    server_socket.listen(5)
    print(f"Server started. Encryption Key (share with clients): {KEY.decode()}")

    client_sockets = []
    try:
        while True:
            client, address = server_socket.accept()
            print(f"Connection established with {address}")
            client_sockets.append(client)
            client.send(KEY)  # Send encryption key to client
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    start_server()
