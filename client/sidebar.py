import streamlit as st
                        #!.......................................................................corrigir, fazer com que o online seja dinamico
                        #!.......................................................................corrigir, fazer com que o numero de notificações e hora da ultima msg sejam dinamicas
def sidebar(user, users, get_json_image, socket_manager):

    #/dados do usuário
    image = get_json_image(user["photo"])
    name = user["name"]
    username = user["username"]

    #/ informações do usuário
    st.sidebar.markdown(
        f"""
        <div style="align-items: center; gap: 10px;">
            <img src="{image}" style="border-radius: 10%; object-fit: cover; width: 300px; height: 300px;">
            <h1 style="font-size:30px; margin: 0;padding: 5px 0px 0px 10px; color: #3f84f0">{username}</h1>
            <p style="font-size: 15px; margin: 0;padding: 0px 0px 0px 10px; color: gray;">olá {name}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("<br>", unsafe_allow_html=True) 
    st.sidebar.success('This is a success message!', icon="✅")

    #/ lista de usuários
    st.sidebar.title("Usuários:")


    for user in users:
        profile_image = get_json_image(user["photo"])
        profile_name = user["name"]
        profile_username = user["username"]


            
        col01, col02 = st.sidebar.columns([1,1])

        with col01:
            st.sidebar.markdown(
                f"""
                <div class="user">
                    <img src="{profile_image}" >
                    <div class="userDetails" style="">
                        <h1>{profile_name}</h1>
                        <p>online</p>
                    </div>
                    <div class="status" >
                        <p>10:40</p>
                        <div class="notification" >
                            <p>2</p>
                        </div>
                    </div>
                </div>
                <style>
                .user{{
                    display: flex; 
                    align-items: center; 
                    gap: 10px;
                    height: 100px;
                    border-radius: 20px;
                    padding: 10px;
                    margin: 0px;
                }}
                .user:hover{{
                }}
                .user img{{
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    object-fit: cover
                }}
                .userDetails{{
                    display: flex; 
                    flex-direction: column; 
                    justify-content: center; 
                    border-radius: 10px; 
                    max-height: 40px; 
                    padding: 5px;
                }}
                .userDetails h1{{
                    margin: 0;
                    padding: 0;
                    # background-color: #f0f0f0;
                }}
                .userDetails p{{
                    margin: 0;
                    padding: 0;
                    font-size: 12px;
                    color: gray;
                }}
                .status{{
                    display: flex;
                    justify-content: flex-end;
                    flex-direction: column;
                    align-items: center;
                    padding: 5px;
                    margin-left: auto;
                }}
                .notification{{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 40px;
                    height: 20px;
                    border-radius: 20px;
                    background-color: #00a884;
                    margin-left: auto;

                }}
                .notification p{{
                    margin: 0;
                    padding: 0;
                    color: white;
                    font-size: 15px;
                    font-weight: bold;
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )

        with col02:
            if st.sidebar.button("iniciar chat", key=profile_username, use_container_width=True):
                st.session_state.chat_init = user
                if st.session_state.chat_messages is not None:
                    socket_manager.send_by_package_dict_to_json({"message": "exit_code_000207000"})
                    st.session_state.chat_messages = None

                

            st.sidebar.markdown("---")  # Linha horizontal


