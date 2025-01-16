class UserService:
    def __init__(self, db):
        self.db = db

    def login(self, username, password):
        try:
            user = self.db.selectUser(username)
            if user:
                if user[3] != password:
                    print(f"Senha incorreta para o usuário {username}.")
                    return False
                print(f"Usuário {username} logado com sucesso.")
                return True
        except Exception as e:
            print(e)
        return False

    def create_user(self, username, name, email, password, phone, photo=None):
        try:
            self.db.insertUser(username, name, email, password, phone, photo)
            print(f"Usuário {username} criado com sucesso.")
            return True
        except Exception as e:
            print(e)
            return False

    def delete_user(self, username):
        try:
            self.db.deleteUser(username)
            print(f"Usuário {username} deletado com sucesso.")
            return True
        except Exception as e:
            print(e)
            return False

    def list_users(self):
        try:
            users = self.db.selectUsers()
            response = []
            for user in users:
                response.append({
                    "username": user[0],
                    "name": user[1],
                    "email": user[2],
                    "phone": user[4],
                    "photo": user[5]
                })
            return response
        except Exception as e:
            return(e)

    def getUser(self, username):
        try:
            user = self.db.selectUser(username)
            response = {
                "username": user[0],
                "name": user[1],
                "email": user[2],
                "phone": user[4],
                "photo": user[5]
            }
            return response
        except Exception as e:
            print(e)
            return False

