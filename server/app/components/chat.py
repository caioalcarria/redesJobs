def chat(socket_manager, user_service, username_session, messages_service, profiles):

    #/função para pegar o socket de algum usuário online
    def get_client_socket_manager(username):
        for profile in profiles.getProfiles():
            if profile["username"] == username:
                return profile["client_socket_manager"]
        return None

    while True:
        #/pegar o usuário que ele quer conversar
        recipient = socket_manager.receive_string()
        #/verificar se o usuário existe na base de dados
        user_recipient = user_service.getUser(recipient)

        if user_recipient:
            #/retornar historico de mensagens
            msg_history = messages_service.list_messages(username_session, recipient)
            socket_manager.send_by_package_dict_to_json(msg_history, 1024 * 10)

            while True:
                #/pegar a mensagem que o usuário deseja enviar
                message = socket_manager.receive_by_package_json_to_dict()
                #/se a mensagem for igual a exit_code_000207000, encerrar a conversa e esperar de novo ser enviado um recipient
                if message['message'] == 'exit_code_000207000':
                    client_socket_manager_self = get_client_socket_manager(username_session)
                    if client_socket_manager_self:
                        client_socket_manager_self.send_by_package_dict_to_json({"message": "exit_code_000207000"})
                    print('Conversa encerrada')
                    break
                else:
                    #/pegar o socket do usuário que está enviando a mensagem e envia uma mensagem para de exit_code_000207000 para ele (lidando com problema do streamlit)
                    client_socket_manager_self = get_client_socket_manager(username_session)
                    if client_socket_manager_self:
                        client_socket_manager_self.send_by_package_dict_to_json({"message": "exit_code_000207000"})

                    #/adicionar a mensagem no banco de dados
                    messages_service.send_message(username_session, recipient, message['message'])

                    #/verificar se o recipient está online e enviar a mensagem para ele
                    client_socket_manager_recipient = get_client_socket_manager(recipient)
                    if client_socket_manager_recipient:
                        print('Mensagem enviada para o recipient online')
                        client_socket_manager_recipient.send_by_package_dict_to_json(message)
                        print('Mensagem recebida de recipient online')
        else:
            error = {"error": "User not found"}
            socket_manager.send_by_package_dict_to_json(error)
