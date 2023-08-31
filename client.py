import socket
import threading

def receive_message(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Received: {message}")

def start_tcp_client(room_name, max_clients):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect(('127.0.0.1', 12345))
    tcp_sock.send(f"{room_name}:{max_clients}".encode('utf-8'))

    receiver_thread = threading.Thread(target=receive_message, args=(tcp_sock,))
    receiver_thread.start()

    while True:
        message = input("Enter your message: ")
        tcp_sock.send(message.encode('utf-8'))

if __name__ == '__main__':
    room_name = input("Enter the room name: ")
    max_clients = input("Enter the maximum number of clients: ")
    start_tcp_client(room_name, max_clients)
