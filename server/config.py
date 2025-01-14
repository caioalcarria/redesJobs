import socket
import threading
import signal
import sys


class IpSend:
    def __init__(self):
        self.onlineAccount = []

    def onlineProfiles(self, client_socket_manager, username):
        for profile in self.onlineAccount:
            if profile["username"] == username:
                profile["client_socket_manager"] = client_socket_manager
                return
        profile = {
            "username": username,
            "client_socket_manager": client_socket_manager
        }
        self.onlineAccount.append(profile)
        
    def getProfile(self, username):
        for profile in self.onlineAccount:
            if profile["username"] == username:
                return profile["client_socket_manager"]
            return None
    def getProfiles(self):
        return self.onlineAccount
profiles = IpSend()









def server_start(function):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12321))
    server.listen(50)
    print("Servidor aguardando conexões...")

##? Sinal para encerrar o servidor
    def signal_handler(sig, frame):
        print('Encerrando o servidor...')
        server.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        client, address = server.accept()
        print(f"Conexão recebida de {address}")
        threading.Thread(target=function, args=(client, profiles)).start()












def message_live_server(function):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12322))
    server.listen(50)
    print("Servidor de mensagens aguardando conexões...")

    while True:
        client, address = server.accept()
        print(f"Conexão recebida de {address}")
        threading.Thread(target=function, args=(client,profiles)).start()