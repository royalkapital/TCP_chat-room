# imports
import socket
import threading
# import time


# functions
def receive():
    while True:
        conn, addr = server.accept()
        conn.send('NAME'.encode(FORMAT))

        nickname = conn.recv(1024).decode(FORMAT)

        with open('bans.txt', 'r') as file:
            bans = file.readlines()

        if nickname+'\n' in bans:
            conn.send('BAN'.encode(FORMAT))
            conn.close()
            continue

        if nickname in nicknames:
            conn.send('USED'.encode(FORMAT))
            continue

        if nickname == 'admin':
            conn.send('PASS'.encode(FORMAT))
            password = conn.recv(1024).decode(FORMAT)

            if password == 'adminpass':
                conn.send('ACCEPT'.encode(FORMAT))
            else:
                conn.send('REFUSE'.encode(FORMAT))
                continue

        nicknames.append(nickname)
        clients.append(conn)

        print(f'Nickname is: {nickname}')

        broadcast(f'{nickname} has joined chat!'.encode(FORMAT))

        conn.send('\n Connection successful!'.encode(FORMAT))

        thread = threading.Thread(target=handle, args=(conn,))
        thread.start()

        print(f'active connections {threading.activeCount() - 1}')


def handle(conn):
    while True:
        try:
            message = conn.recv(1024)
            msg = message.decode(FORMAT)
            if msg.startswith('KICK'):
                if nicknames[clients.index(conn)] == 'admin':
                    name_to_kick = msg[5:]
                    kick_user(name_to_kick, 'kick')
                else:
                    conn.send('Command was refused!'.encode(FORMAT))
            elif msg.startswith('BAN'):
                if nicknames[clients.index(conn)] == 'admin':
                    name_to_ban = msg[4:]
                    kick_user(name_to_ban, 'ban')
                    with open('bans.txt', 'a') as file:
                        file.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    conn.send('Command was refused!'.encode(FORMAT))
            else:
                broadcast(message)
        except:
            if conn in clients:
                index = clients.index(conn)
                clients.pop(index)
                conn.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode(FORMAT))
                print(f'active connections {threading.activeCount() - 1 - 1}')
                nicknames.pop(index)
                break


def kick_user(name, cmd):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin!'.encode(FORMAT))
        # time.sleep(3)
        # client_to_kick.close()
        client_to_kick.send('PENALTY'.encode(FORMAT))
        nicknames.remove(name)
        if cmd == 'ban':
            broadcast(f'{name} was banned by an admin!'.encode(FORMAT))
        elif cmd == 'kick':
            broadcast(f'{name} was kicked by an admin!'.encode(FORMAT))


def broadcast(message):
    for client in clients:
        client.send(message)


# main
if __name__ == '__main__':
    PORT = 9999

    SERVER = socket.gethostbyname(socket.gethostname())

    ADDRESS = (SERVER, PORT)

    FORMAT = 'utf-8'

    clients, nicknames = [], []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen()

    print('Server is working on ' + SERVER)

    receive()
