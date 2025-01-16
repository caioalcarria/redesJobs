def login(user_service, request, socket_manager):
    if user_service.login(request['username'], request['password']):
        response = {"login": True}
        socket_manager.send_dict_to_json(response)
        return request['username']
    else:
        response = {"login": False}
        socket_manager.send_dict_to_json(response)