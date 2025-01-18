import streamlit as st
from socketManager import SocketManager
import json
import base64
import struct

def login(server):
    socket_manager = SocketManager(st.session_state.serverSession)
    
    st.title("Login")
    username = st.text_input("Digite seu username:")
    password = st.text_input("Digite sua senha:", type="password")


    if st.button("Fazer cadastro", type="tertiary"):

        @st.dialog("Cadastrar")
        def Cadastrar():
            username = st.text_input("username")
            name = st.text_input("name")
            email = st.text_input("email")
            password = st.text_input("password", type="password")
            phone = st.text_input("phone")
            photo = st.file_uploader("photo")
            

            if photo is not None:
                photo_bytes = photo.read()
                encoded_file = base64.b64encode(photo_bytes).decode('utf-8')
                photo_data = {
                    "filename": photo.name,
                    "filetype": photo.type,
                    "file": encoded_file
                }
                photo = json.dumps(photo_data)


            if st.button("Submit"):
                with st.spinner('Wait for it...'):
                    data = {"action": "register", "username": username, "name": name, "email": email, "password": password, "phone": phone, "photo": photo}

                    socket_manager.send_by_package_dict_to_json(data, 4)

                    response = socket_manager.receive_json_to_dict()

                    if response['register']:
                        st.balloons()
                        st.success("Cadastro realizado com sucesso!")
                    elif not response['register']:
                        st.error("Erro ao cadastrar")
        
        Cadastrar()

    
    if st.button("Login", use_container_width=True , type="primary"):
        with st.spinner('Wait for it...'):
            data = {"action": "login", "username": username, "password": password}
            socket_manager.send_by_package_dict_to_json(data)

            response = socket_manager.receive_json_to_dict()

            if response['login']:
                st.success("Login realizado com sucesso!")
                return username
            elif not response['login']:
                st.error("Usuário ou senha incorretos")
                return False

