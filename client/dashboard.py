import streamlit as st
from socketManager import SocketManager
from sidebar import sidebar
from chat import chat
import json
import base64
import struct
import time

def dashboard(server, user_info, messageLiveServerSocketManager, live_messages):
    socket_manager = SocketManager(server)    

    st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/1200px-Google_2015_logo.svg.png", size="large")


    #/estados
    if 'chat_init' not in st.session_state:
        st.session_state.chat_init = False

    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = None
    

    #/tratamento de imagem DB
    def get_json_image(photo):
        if photo is not None:
            photo_data = json.loads(photo)
            return f"data:image/jpeg;base64,{photo_data['file']}"
        return None

    #/lista de usuarios
    users = st.session_state.users_list


    #/?renderização da sidebar
    sidebar(user_info, users, get_json_image, socket_manager)







    def mainDashboard():
        st.title("Chat")
        st.write("Você pode enviar mensagens para o chat e elas serão exibidas aqui.")
        st.write("Para enviar uma mensagem, basta digitar no campo abaixo e clicar em 'Enviar'.")
        st.write("Você também pode usar emojis para adicionar um toque de humor ao seu texto. 😄")


    chat_init = st.session_state.chat_init

    if chat_init == False:
        mainDashboard()
    else:
        rerun_chat = chat(chat_init, user_info, get_json_image, socket_manager, messageLiveServerSocketManager, live_messages)
