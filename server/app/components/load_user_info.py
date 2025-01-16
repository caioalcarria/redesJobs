def loadUserInfo(socket_manager, user_service, username_seasson):
        

        request_user_info = socket_manager.receive_string()
        
        if request_user_info == 'get_user_info':

            user_info = user_service.getUser(username_seasson)

            socket_manager.send_by_package_dict_to_json(user_info, 1024 * 10)

        else:
            error = {"error": "Invalid request"}
            socket_manager.send_by_package_dict_to_json(error)