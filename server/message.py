class MessageService:
    def __init__(self, db):
        self.db = db

    def send_message(self, sender, recipient, message):
        try:
            self.db.insertMessage(sender, recipient, message)
            print(f"Mensagem enviada de {sender} para {recipient}.")
            return True
        except Exception as e:
            print(e)
            return False

    def update_message(self, id, element, data):
        try:
            self.db.updateMessage(id, element, data)
            print(f"Mensagem {id} atualizada.")
            return True
        except Exception as e:
            print(e)
            return False

    def list_messages(self, username, recipient):
        try:
            messages = self.db.selectUserChat(username, recipient)
            messages_json = []
            for message in messages:
                messages_json.append({
                    "id": message[0],
                    "sender": message[1],
                    "recipient": message[2],
                    "view": message[3],
                    "message": message[4],
                    "media": message[5],
                    "time": message[6]
                })
            return messages_json
        except Exception as e:
            print(e)
            return []

    def get_message(self, id):
        try:
            message = self.db.selectMessage(id)
            print(message)
        except Exception as e:
            print(e)

