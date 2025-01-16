import socket
import threading
from online_profiles import Profiles


profiles = Profiles()


def server_start(function):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 1234))
    server.listen(50)
    print("Servidor aguardando conexões...")

    while True:
        client, address = server.accept()
        print(f"Conexão recebida de {address}")
        threading.Thread(target=function, args=(client, profiles)).start()




def message_live_start(function):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 1235))
    server.listen(50)
    print("Servidor de mensagens aguardando conexões...")

    while True:
        client, address = server.accept()
        print(f"Conexão recebida de {address}")
        threading.Thread(target=function, args=(client,profiles)).start()