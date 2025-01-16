from database.services.users import UserService
from database.services.message import MessageService
from database.db import db
from socketManager import SocketManager

from app.components.login import login
from app.components.register import register
from app.components.load_user_info import loadUserInfo
from app.components.load_users_list import loadUsersList
from app.components.chat import chat




def server_client_handle(client_socket, profiles):
    user_service = UserService(db())
    messages_service = MessageService(db())
    socket_manager = SocketManager(client_socket)
    username_seasson = None

    try:
        #/loop para realizar o login ou cadastro
        while True:
            request = socket_manager.receive_by_package_json_to_dict()

            if request['action'] == 'register':
                register(user_service, request, socket_manager)

            elif request['action'] == 'login':
                if login(user_service, request, socket_manager):
                    username_seasson = request['username']
                    break

        #/ request para carregar informações do usuário logado
        loadUserInfo(socket_manager, user_service, username_seasson)

        #/ request para carregar lista de usuários
        loadUsersList(socket_manager, user_service)

        #/ request para iniciar loop do chat

        chat(socket_manager, user_service, username_seasson, messages_service, profiles)


    except Exception as error:
        print(error)
