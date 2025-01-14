import sqlite3


class db:
    def __init__(self):
        self.conn = sqlite3.connect('database/db.sqlite')
        self.cursor = self.conn.cursor()

        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (username VARCHAR(20) PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, phone VARCHAR(20) NOT NULL UNIQUE, photo JSON)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender VARCHAR(20) NOT NULL, recipient VARCHAR(20) NOT NULL,view INTEGER NOT NULL, message TEXT NOT NULL, media JSON , timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (sender) REFERENCES users(username), FOREIGN KEY (recipient) REFERENCES users(username))')

#    user ....................................................
    def insertUser(self, username, name, email, password, phone, photo=None):
        self.cursor.execute('INSERT INTO users (username, name, email, password, phone, photo) VALUES (?, ?, ?, ?, ?, ?)', (username, name, email, password, phone, photo))
        self.conn.commit()

    def updateUser(self, username, element, data):
        self.cursor.execute(f'UPDATE users SET {element} = ? WHERE username = {username}', (data, ))
        self.conn.commit()

    def deleteUser(self, username):
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username, ))
        self.conn.commit()

    def selectUser(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username, ))
        return self.cursor.fetchone()

    def selectUsers(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

#    message ....................................................
    def insertMessage(self, sender, recipient, message, view=False, media=None):
        self.cursor.execute('INSERT INTO messages (sender, recipient, view, message, media) VALUES (?, ?, ?, ?, ?)', (sender, recipient, view, message, media))
        self.conn.commit()

    def updateMessage(self, id, element, data):
        self.cursor.execute(f'UPDATE messages SET {element} = ? WHERE id = {id}', (data, ))
        self.conn.commit()

    def selectUserChat(self, username, recipient):
        self.cursor.execute('SELECT * FROM messages WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)', (username, recipient, recipient, username))
        return self.cursor.fetchall()

    def selectMessage(self, id):
        self.cursor.execute('SELECT * FROM messages WHERE id = ?', (id, ))
        return self.cursor.fetchone()

    def __del__(self):
        self.conn.close()
