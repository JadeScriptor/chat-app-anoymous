import socket
import threading

ip = "127.0.0.1"
port = 5555


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            print(f'{username} left the chat')
            usernames.remove(username)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')
        client.send('NICK'.encode("ascii"))
        nickname = client.recv(1024).decode('ascii')
        print(nickname)
        usernames.append(nickname)
        clients.append(client)

        print(f"Nickname of user is {nickname}")
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('connected the server DARKCHAT'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("server is listening")
receive()
