import streamlit as st
from datetime import datetime
import threading
import time




def chat(user_chat, user, get_json_image, socket_manager, messageLiveServerSocketManager, live_messages):
    
    #/estado
    if 'chat_messages_online' not in st.session_state:
        st.session_state.chat_messages_online = True

    #/informções do user_chat
    user_chat_name = user_chat['name']
    user_chat_username = user_chat['username']
    user_chat_image = get_json_image(user_chat['photo'])

    #/informações do usuario logado
    user_name = user['name']
    user_username = user['username']
    user_image = get_json_image(user['photo'])


    #/nome do usuario com quem quero conversar
    st.title(user_chat_name)


    #/funções do elementos de chat 
    def mensagem_enviada(message):
        message_str = message["message"]
        time = message["time"]

        with st.chat_message('user', avatar=user_image):
            
            col1, col2 = st.columns([12,1])

            with col1:
                st.write(message_str)

            with col2:
                st.write(time.split(' ')[1][:5])

            col1, col2 = st.columns([15, 1])  # Ajuste as proporções conforme necessário

            with col1:
                ...

            with col2:
                st.image("https://cdn-icons-png.flaticon.com/256/8369/8369113.png", width=20)


    def mensagem_recebida(message):
        message_str = message["message"]
        time = message["time"]

        with st.chat_message("assistant", avatar=user_chat_image):
            
            col1, col2 = st.columns([10,1])

            with col1:
                st.write(message_str)

            with col2:
                st.write(time.split(' ')[1][:5])


    #/função para rederizar as mensagens
    def render_messages():
        if st.session_state.chat_messages == []:
            st.write("Nenhuma mensagem")
        else:
            for message in st.session_state.chat_messages:
                if message["sender"] == user_username:
                    mensagem_enviada(message)
                else:
                    mensagem_recebida(message)

    #! o problema é que isso n pode se repetir..............................................................

    if st.session_state.chat_messages == None:

        #/mandando do servidor com quem eu quero conversar
        socket_manager.send_string(user_chat_username)

        #/recebendo array do servidor com historico de mensagens
        messages = socket_manager.receive_by_package_json_to_dict()

        #/adicionando array de mensagens no estado
        st.session_state.chat_messages = messages

        render_messages()


    chat_messages = st.session_state.chat_messages
    #! o problema é que isso n pode se repetir..............................................................



    #/campo de texto para enviar mensagem
    prompt = st.chat_input("Say something")
    if prompt:
        st.session_state.chat_messages_online = False
        print("enviandddddddddooooo")
        #/criando um dicionario com a mensagem
        message = {"sender": user_username, "message": prompt, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        #/adicionando a mensagem no estado
        st.session_state.chat_messages.append(message)
        #/enviando mensagem para o servidor
        socket_manager.send_by_package_dict_to_json(message)
        #/renderizando a mensagem
        render_messages()


    #/recebendo mensagem do servidor


    while True:

        message_rec = messageLiveServerSocketManager.receive_by_package_json_to_dict()
        print("mensagem recebida fora do botão")
        print(message_rec)

        if message_rec["message"] == "exit_code_000207000":
            break
        elif message_rec["sender"] == user_chat_username :
            st.session_state.chat_messages.append(message_rec)
            #?so rederiza a msgns em sí
            mensagem_recebida(message_rec)
        else:
            pass

    return True