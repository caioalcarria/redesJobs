class Profiles:
    def __init__(self):
        self.onlineAccount = []

    def onlineProfiles(self, client_socket_manager, username):
        for profile in self.onlineAccount:
            if profile["username"] == username:
                profile["client_socket_manager"] = client_socket_manager
                return
        profile = {
            "username": username,
            "client_socket_manager": client_socket_manager
        }
        self.onlineAccount.append(profile)
        
    def getProfile(self, username):
        for profile in self.onlineAccount:
            if profile["username"] == username:
                return profile["client_socket_manager"]
            return None
    def getProfiles(self):
        return self.onlineAccount
    
profiles = Profiles()