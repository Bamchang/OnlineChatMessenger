import socket
import threading

class ChatRoom:
    def __init__(self, name, max_clients):
        self.name = name
        self.max_clients = max_clients
        self.clients = []

    def broadcast(self, message, from_client):
        for client in self.clients:
            if client != from_client:
                client.send(message.encode('utf-8'))

chat_rooms = {}

def handle_client(client_socket):
    room_name, max_clients = client_socket.recv(1024).decode('utf-8').split(':')
    max_clients = int(max_clients)

    if room_name not in chat_rooms:
        chat_rooms[room_name] = ChatRoom(room_name, max_clients)

    chat_room = chat_rooms[room_name]

    if len(chat_room.clients) >= chat_room.max_clients:
        client_socket.send("Room is full".encode('utf-8'))
        return

    chat_room.clients.append(client_socket)
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        chat_room.broadcast(message, client_socket)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(5)

while True:
    client_socket, _ = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
