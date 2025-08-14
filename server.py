import socket
import threading

HOST = "127.0.0.1"  # Mahalliy IP
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Xabar yuborish
def broadcast(message):
    for client in clients:
        client.send(message)

# Klientdan xabar olish
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} chatdan chiqdi!\n".encode("utf-8"))
            nicknames.remove(nickname)
            break

# Yangi ulanishlar
def receive():
    while True:
        client, address = server.accept()
        print(f"{str(address)} ulanmoqda...")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname: {nickname}")
        broadcast(f"{nickname} chatga qo‘shildi!\n".encode("utf-8"))
        client.send("Serverga ulanding!\n".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server ishga tushdi...")
receive()
