import socket
from cryptography.fernet import Fernet
import threading

def receive_messages(client_socket, cipher):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if encrypted_message:
                decrypted_message = cipher.decrypt(encrypted_message).decode()
                print(f"Server: {decrypted_message}")
            else:
                break
        except:
            print("Connection closed.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    # Receive encryption key from server
    KEY = client_socket.recv(1024)
    cipher = Fernet(KEY)
    print("Encryption key received. Secure communication established.")

    # Start thread for receiving messages
    thread = threading.Thread(target=receive_messages, args=(client_socket, cipher))
    thread.start()

    # Send encrypted messages
    try:
        while True:
            message = input("You: ")
            encrypted_message = cipher.encrypt(message.encode())
            client_socket.send(encrypted_message)
    except KeyboardInterrupt:
        print("Closing connection...")
        client_socket.close()

if __name__ == "__main__":
    start_client()
