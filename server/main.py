from config import server_start
from users import UserService
from message import MessageService
from database.db import db
from socketManager import SocketManager
from message_live_server import message_live_client_handle
from config import message_live_server
import threading
import json
import struct

def server_client_handle(client_socket, profiles):
    users = UserService(db())
    messages = MessageService(db())
    socket_manager = SocketManager(client_socket)
    userSeasson = None

    try:
        while True:

            request = socket_manager.receive_by_package_json_to_dict()

            if request['action'] == 'login':

                if users.login(request['username'], request['password']):
                    response = {"login": True}
                    socket_manager.send_dict_to_json(response)
                    userSeasson = request['username']
                    break
                else:
                    response = {"login": False}
                    socket_manager.send_dict_to_json(response)

            elif request['action'] == 'register':

                if users.create_user(request['username'], request['name'], request['email'], request['password'], request['phone'], request['photo']):
                    response = {"register": True}
                    socket_manager.send_dict_to_json(response)
                else:
                    response = {"register": False}
                    socket_manager.send_dict_to_json(response)


        # / request para carregar informações do usuário logado
        request_user_info = socket_manager.receive_string()
        if request_user_info == 'get_user_info':

            user_info = users.getUser(userSeasson)

            socket_manager.send_by_package_dict_to_json(user_info, 1024 * 10)

        else:
            error = {"error": "Invalid request"}
            socket_manager.send_by_package_dict_to_json(error)

        

        # / request para listar usuários
        request_user_list = socket_manager.receive_string()
        if request_user_list == 'get_users_list':
            user_list = users.list_users()
            socket_manager.send_by_package_dict_to_json(user_list, 1024 * 10)


        else:
            error = {"error": "Invalid request"}
            socket_manager.send_by_package_dict_to_json(error)



        while True:
            #/request para identificar se usuário que ele quer conversar existe:
            recipient = socket_manager.receive_string()

            user_recipient = users.getUser(recipient)

            if user_recipient:
                #/ retornar historico de msg
                msg_history = messages.list_messages(userSeasson,recipient)
                socket_manager.send_by_package_dict_to_json(msg_history, 1024 * 10)




                while True:
                    message = socket_manager.receive_by_package_json_to_dict()
                    if message['message'] == 'exit_code_000207000':
                        online_profiles_list = profiles.getProfiles()

                        client_socket_manager_self = None

                        for profile in online_profiles_list:
                            if profile["username"] == userSeasson:
                                client_socket_manager_self = profile["client_socket_manager"]

                        client_socket_manager_self.send_by_package_dict_to_json({"message": "exit_code_000207000"})

                        print('Conversa encerrada')
                        break
                    else:
                        #/quando eu receber a msgn que ele quer enviar eu tenho que mandar uma mensagem de volta para ele pra informar que a mensagem foi enviada 
                        #/ essa mensagem vai ser enviada no outro socket dele que está aberto esperando pra recerber a mensagem
                        #/ isso pra dizer avisar ao cliente que agora ele está envando msgn e pode fechar o whille de espera de mensagem pra pode reinstanciar o while de espera de mensagem

                        #pega o socket do aberto do meu cliente
                        online_profiles_list = profiles.getProfiles()

                        client_socket_manager_self = None

                        for profile in online_profiles_list:
                            if profile["username"] == userSeasson:
                                client_socket_manager_self = profile["client_socket_manager"]

                        client_socket_manager_self.send_by_package_dict_to_json({"message": "exit_code_000207000"})

                        

                        


                        #/ adicionar msgn ao bando de dados
                        messages.send_message(userSeasson, recipient, message['message'])

                        #? verificar se o usuário está online
                        # print('varificar se usuário foi encontraado no online')
                        # print(profiles.getProfiles())
                        # client_socket_manager_recipient = profiles.getProfile(recipient)

                        client_socket_manager_recipient = None

                        #? pega a desgraça dos usuários online
                        online_profiles_list = profiles.getProfiles()
                        for profile in online_profiles_list:
                            if profile["username"] == recipient:
                                client_socket_manager_recipient = profile["client_socket_manager"]
                        

                        #/ enviar msg para a thread do cliente do recipient via socket (esse socket só está disponivel se ele estiver online)
                        if client_socket_manager_recipient:
                            #........................aqui o codigo para enviar a mensagem para o socket do recipient
                            print('Mensagem enviada para o recipient online')
                            client_socket_manager_recipient.send_by_package_dict_to_json(message)
                            print('Mensagem recebida de recipient online')
                            #!quando o usuário deslogar eu tenho que remover o socket dele da lista de profiles
                        else:
                            pass
            else:
                error = {"error": "User not found"}
                socket_manager.send_by_package_dict_to_json(error)




        # if users.getUser(response):
        #     client_socket.send('Conversa iniciada'.encode('utf-8'))
        #     chat = messages.list_messages(user_name, response)
        #     for message in chat:
        #         print(message)
        #         client_socket.send(f"{message[1]} - {message[4]}\n".encode('utf-8'))
        #     while True:
        #         client_socket.send('Digite sua mensagem: '.encode('utf-8'))
        #         msg = client_socket.recv(1024).decode('utf-8')
        #         messages.send_message(user_name, response, msg)
        #         recipient = profiles.getProfile(response)

        #         if recipient:
        #             recipient.send(f"{msg}".encode('utf-8'))
        #         else:
        #             client_socket.send('Usuário offline'.encode('utf-8'))


        #         #preciso verificar se o usuário está online e enviar a mensagem para ele caso esteja
        #        #quando o usuário se conectar eu tenho que salvar o ip dele de alguma forma
        #        #preciso criar um método para verificar se o usuário está online
        #        #preciso criar um método para enviar a mensagem para o usuário
        #        #preciso criar um método para receber a mensagem do usuário
        # else:
        #     client_socket.send('Usuário não existe'.encode('utf-8'))

        # # carregar o chat das duas pessoas
        # # Conectar as duas para conexão direta

    except Exception as error:
        print(error)

threading.Thread(target=message_live_server, args=(message_live_client_handle,)).start()

server_start(server_client_handle)
