from config import message_live_server
from socketManager import SocketManager

def message_live_client_handle(client_socket, profiles):
    socket_manager = SocketManager(client_socket)
    print("Conexão estabelecida com o servidor de mensagens")

    #/ qual o user que está conectado
    username = socket_manager.receive_string()
    print(f"Usuário {username} conectado ao servidor de mensagens")

    #/ adiciona na lista de perfis onlines
    profiles.onlineProfiles(socket_manager, username)
    print(profiles.getProfiles())


    #/se username tiver lá, tira o perfil da lista e coloca o novo

