def loadUsersList(socket_manager, user_service):
    request_user_list = socket_manager.receive_string()

    if request_user_list == 'get_users_list':
        user_list = user_service.list_users()
        socket_manager.send_by_package_dict_to_json(user_list, 1024 * 10)

    else:
        error = {"error": "Invalid request"}
        socket_manager.send_by_package_dict_to_json(error)
