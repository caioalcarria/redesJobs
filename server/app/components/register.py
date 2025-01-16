def register(user_service, request, socket_manager):
    
    if user_service.create_user(request['username'], request['name'], request['email'], request['password'], request['phone'], request['photo']):
        response = {"register": True}
        socket_manager.send_dict_to_json(response)
    else:
        response = {"register": False}
        socket_manager.send_dict_to_json(response)