import socket
import streamlit as st
from login import login
from dashboard import dashboard
from socketManager import SocketManager
import threading


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.serverSession = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    st.session_state.serverConnect = st.session_state.serverSession.connect(('127.0.0.1', 12317))

socket_manager = SocketManager(st.session_state.serverSession)

if  st.session_state.logged_in == True:
    if 'user_info' not in st.session_state:
        socket_manager.send_string("get_user_info")
        data = socket_manager.receive_by_package_json_to_dict()
        st.session_state.user_info = data

        socket_manager.send_string("get_users_list")
        data = socket_manager.receive_by_package_json_to_dict()
        st.session_state.users_list = data

    if 'live_messages' not in st.session_state:
        st.session_state.live_messages = []
        st.session_state.messageLiveServerSession = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        st.session_state.messageLiveServerConnect = st.session_state.messageLiveServerSession.connect(('127.0.0.1', 12318))
        st.session_state.messageLiveServerSocketManager = SocketManager(st.session_state.messageLiveServerSession)
        st.session_state.messageLiveServerSocketManager.send_string(st.session_state.user_info['username'])

    # def receive_messages(messageLiveServerSocketManager, live_messages, st):
    #     while True:
    #         print("rodo dnvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    #         message_rec = messageLiveServerSocketManager.receive_by_package_json_to_dict()
    #         live_messages.append(message_rec)
    #         print(live_messages)
    #         st.rerun()
            
    # threading.Thread(target=receive_messages, args=(st.session_state.messageLiveServerSocketManager, st.session_state.live_messages, st)).start()


try:
    server = st.session_state.serverSession

    if not st.session_state.logged_in:
        username = login(server)
        if username:
            st.session_state.logged_in = True
            st.rerun()
    if st.session_state.logged_in:
        dashboard(server, st.session_state.user_info, st.session_state.messageLiveServerSocketManager, st.session_state.live_messages)
    
except socket.error as e:
    st.error(f"Internal server error: {e}")
